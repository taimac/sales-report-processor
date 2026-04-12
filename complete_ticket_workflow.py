"""
Automate the SRP post-ticket workflow.

Flow:
1. Push current feature branch
2. Open PR if needed
3. Close current Jira ticket with a comment
4. Move next Jira ticket to In Progress
5. Refresh Jira backlog markdown
6. Update AI context Jira Structure and Backlog Order
7. Commit refreshed docs
8. Merge PR
9. Checkout dev
10. Pull origin dev
11. Delete merged feature branch locally and remotely

This script is intentionally explicit. It can run as a dry-run first and
requires the current/next ticket keys to avoid risky guesses.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from jira import JIRA


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
BACKLOG_FILE = DOCS_DIR / "jira_backlog_SRP.md"
AI_CONTEXT_FILE = DOCS_DIR / "AI" / "AI_CONTEXT_SRP.md"

load_dotenv(BASE_DIR / ".env")

JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "").strip('"')
JIRA_TOKEN = os.environ.get("JIRA_TOKEN", "").strip('"')
JIRA_DOMAIN = os.environ.get("JIRA_DOMAIN", "").strip('"')
JIRA_PROJECT = os.environ.get("JIRA_PROJECT", "SRP").strip('"')
JIRA_URL = f"https://{JIRA_DOMAIN}" if JIRA_DOMAIN else ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automate the SRP ticket workflow.")
    parser.add_argument("--current-ticket", required=True, help="Current Jira ticket, e.g. SRP-30")
    parser.add_argument(
        "--next-ticket",
        help="Next Jira ticket to move into progress. Optional when docs/jira_backlog_SRP.md contains Execution Order.",
    )
    parser.add_argument("--jira-comment", required=True, help="Close comment to add to the current Jira ticket")
    parser.add_argument(
        "--base-branch",
        default="dev",
        help="Base branch used for PR merge and sync. Default: dev",
    )
    parser.add_argument(
        "--merge-method",
        choices=["merge", "squash", "rebase"],
        default="merge",
        help="PR merge strategy. Default: merge",
    )
    parser.add_argument(
        "--delete-branch",
        action="store_true",
        help="Delete the merged feature branch locally and remotely at the end",
    )
    parser.add_argument(
        "--create-pr",
        action="store_true",
        help="Create a PR if one does not exist",
    )
    parser.add_argument(
        "--pr-title",
        help="Explicit PR title when using --create-pr",
    )
    parser.add_argument(
        "--pr-body",
        help="Explicit PR body when using --create-pr",
    )
    parser.add_argument(
        "--docs-commit-message",
        default="Refresh Jira backlog and AI context",
        help="Commit message for backlog/context updates",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print steps without executing them",
    )
    return parser.parse_args()


def require_env() -> None:
    missing = []
    if not JIRA_EMAIL:
        missing.append("JIRA_EMAIL")
    if not JIRA_TOKEN:
        missing.append("JIRA_TOKEN")
    if not JIRA_DOMAIN:
        missing.append("JIRA_DOMAIN")
    if missing:
        raise SystemExit(f"Missing Jira env vars: {', '.join(missing)}")


def run(cmd: list[str], *, dry_run: bool = False, capture_output: bool = False) -> str:
    printable = " ".join(cmd)
    print(f"$ {printable}")
    if dry_run:
        return ""

    completed = subprocess.run(
        cmd,
        cwd=BASE_DIR,
        text=True,
        capture_output=capture_output,
        check=True,
    )
    if capture_output:
        return completed.stdout.strip()
    return ""


def current_branch(*, dry_run: bool = False) -> str:
    if dry_run:
        return "feature/SRP-XXX-description"
    return run(["git", "branch", "--show-current"], capture_output=True).strip()


def jira_client() -> JIRA:
    require_env()
    return JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))


def get_issue_transition_id(issue, target_names: Iterable[str]) -> str | None:
    target_set = {name.lower() for name in target_names}
    for transition in issue.transitions():
        if transition["name"].lower() in target_set:
            return transition["id"]
    return None


def add_comment_and_transition(
    jira: JIRA,
    ticket_key: str,
    *,
    comment: str | None,
    target_transition_names: Iterable[str],
    dry_run: bool,
) -> None:
    print(f"Updating Jira ticket {ticket_key}")
    if dry_run:
        return

    issue = jira.issue(ticket_key)
    if comment:
        jira.add_comment(ticket_key, comment)

    transition_id = get_issue_transition_id(issue, target_transition_names)
    if transition_id is None:
        raise RuntimeError(
            f"Could not find transition for {ticket_key}. "
            f"Expected one of: {', '.join(target_transition_names)}"
        )
    jira.transition_issue(ticket_key, transition_id)


def parse_execution_order(backlog_text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    pattern = re.compile(
        r"^\| (\d+) \| (story|subtask) \| (SRP-\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$",
        flags=re.MULTILINE,
    )
    for match in pattern.finditer(backlog_text):
        entries.append(
            {
                "order": match.group(1),
                "level": match.group(2),
                "key": match.group(3),
                "parent": match.group(4),
                "summary": match.group(5),
                "status": match.group(6),
                "sprint": match.group(7),
            }
        )
    return entries


def derive_next_ticket(execution_order: list[dict[str, str]], current_ticket: str) -> str:
    current_entry = next((entry for entry in execution_order if entry["key"] == current_ticket), None)
    if current_entry is None:
        raise RuntimeError(f"Current ticket {current_ticket} was not found in Execution Order")

    if current_entry["level"] == "subtask" and current_entry["parent"]:
        found_current = False
        for entry in execution_order:
            if entry["key"] == current_ticket:
                found_current = True
                continue
            if (
                found_current
                and entry["level"] == "subtask"
                and entry["parent"] == current_entry["parent"]
                and entry["status"].lower() != "done"
            ):
                return entry["key"]

        found_parent = False
        for entry in execution_order:
            if entry["key"] == current_entry["parent"]:
                found_parent = True
                continue
            if found_parent and entry["level"] == "story" and entry["status"].lower() != "done":
                return entry["key"]
    else:
        found_current = False
        for entry in execution_order:
            if entry["key"] == current_ticket:
                found_current = True
                continue
            if found_current and entry["level"] == "story" and entry["status"].lower() != "done":
                return entry["key"]

    raise RuntimeError(f"Could not derive the next ticket after {current_ticket}")


def build_jira_structure(execution_order: list[dict[str, str]], current_ticket: str) -> str:
    done = {entry["key"] for entry in execution_order if entry["status"].lower() == "done"}

    def marker(ticket_key: str) -> str:
        if ticket_key == current_ticket:
            return "⬜ ← current"
        if ticket_key in done:
            return "✅ Done"
        return "⬜ To Do"

    epic_summary = next(
        (entry["summary"] for entry in execution_order if entry["key"] == "SRP-2"),
        "Sales Report Processor MVP",
    )
    top_level = [
        entry for entry in execution_order
        if entry["level"] == "story" and entry["key"] != "SRP-2"
    ]
    child_map: dict[str, list[dict[str, str]]] = {}
    for entry in execution_order:
        if entry["level"] == "subtask" and entry["parent"]:
            child_map.setdefault(entry["parent"], []).append(entry)

    lines = ["```", f"[Epic]  SRP-2 – {epic_summary}"]

    for index, entry in enumerate(top_level):
        branch = "└─" if index == len(top_level) - 1 else "├─"
        key = entry["key"]
        summary = entry["summary"]
        lines.append(f"  {branch} {key:<8} {summary:<35} {marker(key)}")
        children = child_map.get(key, [])
        if children:
            for child_index, child in enumerate(children):
                child_branch = "└─" if child_index == len(children) - 1 else "├─"
                child_key = child["key"]
                child_summary = child["summary"]
                lines.append(f"  │    {child_branch} {child_key:<8} {child_summary:<35} {marker(child_key)}")

    lines.append("```")
    return "\n".join(lines)


def build_backlog_order(execution_order: list[dict[str, str]], current_ticket: str) -> str:
    numbered: list[str] = []
    rank = 1
    for entry in execution_order:
        key = entry["key"]
        summary = entry["summary"]
        status = entry["status"]
        if key == "SRP-2" or entry["level"] == "subtask":
            continue
        label = f"{key} – {summary}"
        if status.lower() == "done":
            numbered.append(f"{rank}. ~~{label}~~ ✅ Done")
        elif key == current_ticket:
            numbered.append(f"{rank}. {label}  ← current")
        else:
            numbered.append(f"{rank}. {label}")
        rank += 1
    return "\n".join(numbered)


def replace_section(text: str, heading: str, replacement_body: str) -> str:
    pattern = rf"(## {re.escape(heading)}\n\n)(.*?)(\n---|\Z)"
    replaced, count = re.subn(
        pattern,
        lambda match: f"{match.group(1)}{replacement_body}{match.group(3)}",
        text,
        flags=re.DOTALL,
    )
    if count != 1:
        raise RuntimeError(f"Could not update section: {heading}")
    return replaced


def refresh_ai_context(current_ticket: str, *, dry_run: bool) -> None:
    backlog_text = BACKLOG_FILE.read_text(encoding="utf-8")
    execution_order = parse_execution_order(backlog_text)
    if not execution_order:
        raise RuntimeError("Could not parse Execution Order from docs/jira_backlog_SRP.md")

    ai_context_text = AI_CONTEXT_FILE.read_text(encoding="utf-8")
    ai_context_text = replace_section(
        ai_context_text,
        "Jira Structure",
        build_jira_structure(execution_order, current_ticket),
    )
    ai_context_text = replace_section(
        ai_context_text,
        "Backlog Order",
        build_backlog_order(execution_order, current_ticket),
    )

    print(f"Updating {AI_CONTEXT_FILE}")
    if not dry_run:
        AI_CONTEXT_FILE.write_text(ai_context_text, encoding="utf-8")


def pr_exists(branch_name: str, *, dry_run: bool) -> bool:
    if dry_run:
        return False
    try:
        run(
            ["gh", "pr", "view", branch_name, "--json", "number"],
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def has_doc_changes(*, dry_run: bool) -> bool:
    if dry_run:
        return True
    output = run(
        ["git", "status", "--short", "docs/jira_backlog_SRP.md", "docs/AI/AI_CONTEXT_SRP.md"],
        capture_output=True,
    )
    return bool(output.strip())


def main() -> None:
    args = parse_args()
    branch_name = current_branch(dry_run=args.dry_run)

    if branch_name == args.base_branch:
        raise SystemExit("Refusing to run on the base branch. Checkout your feature branch first.")

    print(f"Current branch: {branch_name}")
    print(f"Current ticket: {args.current_ticket}")

    backlog_text = BACKLOG_FILE.read_text(encoding="utf-8")
    execution_order = parse_execution_order(backlog_text)
    if args.next_ticket:
        next_ticket = args.next_ticket
    elif execution_order:
        next_ticket = derive_next_ticket(execution_order, args.current_ticket)
    else:
        raise RuntimeError(
            "Could not derive the next ticket because docs/jira_backlog_SRP.md "
            "does not contain an Execution Order section yet. Pass --next-ticket once, "
            "or refresh the backlog with the updated exporter."
        )
    print(f"Next ticket: {next_ticket}")

    run(["git", "push", "-u", "origin", branch_name], dry_run=args.dry_run)

    if args.create_pr and not pr_exists(branch_name, dry_run=args.dry_run):
        pr_title = args.pr_title or f"{args.current_ticket}: complete ticket work"
        pr_body = args.pr_body or f"Automated workflow PR for {args.current_ticket}."
        run(
            [
                "gh",
                "pr",
                "create",
                "--base",
                args.base_branch,
                "--head",
                branch_name,
                "--title",
                pr_title,
                "--body",
                pr_body,
            ],
            dry_run=args.dry_run,
        )

    jira = None if args.dry_run else jira_client()
    if jira is not None:
        add_comment_and_transition(
            jira,
            args.current_ticket,
            comment=args.jira_comment,
            target_transition_names=("Done",),
            dry_run=args.dry_run,
        )
        add_comment_and_transition(
            jira,
            next_ticket,
            comment=None,
            target_transition_names=("In Progress",),
            dry_run=args.dry_run,
        )
    else:
        print("Skipping Jira mutations in dry-run mode")

    run([sys.executable, "fetch_jira_backlog_srp.py"], dry_run=args.dry_run)
    refresh_ai_context(next_ticket, dry_run=args.dry_run)

    if has_doc_changes(dry_run=args.dry_run):
        run(
            ["git", "add", "docs/jira_backlog_SRP.md", "docs/AI/AI_CONTEXT_SRP.md"],
            dry_run=args.dry_run,
        )
        run(["git", "commit", "-m", args.docs_commit_message], dry_run=args.dry_run)
        run(["git", "push"], dry_run=args.dry_run)
    else:
        print("No backlog/context doc changes to commit")

    run(
        [
            "gh",
            "pr",
            "merge",
            branch_name,
            f"--{args.merge_method}",
        ],
        dry_run=args.dry_run,
    )

    run(["git", "checkout", args.base_branch], dry_run=args.dry_run)
    run(["git", "pull", "origin", args.base_branch], dry_run=args.dry_run)

    if args.delete_branch:
        run(["git", "branch", "-d", branch_name], dry_run=args.dry_run)
        run(["git", "push", "origin", "--delete", branch_name], dry_run=args.dry_run)

    print("Workflow complete.")


if __name__ == "__main__":
    main()
