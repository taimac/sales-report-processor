"""
Fetch Jira backlog for SRP and export to Markdown.

Purpose:
    Export all Jira issues for the configured SRP project into a Markdown file
    optimized for backlog review and MVP planning.

Output includes:
    - Key
    - Summary
    - Status
    - Created
    - Updated
    - Sprint
    - Description
    - Comments

Usage:
    python fetch_jira_backlog_srp.py
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from jira import JIRA

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(exist_ok=True)

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

# Jira configuration
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "").strip('"')
JIRA_TOKEN = os.environ.get("JIRA_TOKEN", "").strip('"')
JIRA_DOMAIN = os.environ.get("JIRA_DOMAIN", "").strip('"')
JIRA_PROJECT = os.environ.get("JIRA_PROJECT", "SRP").strip('"')

# Construct Jira URL
JIRA_URL = f"https://{JIRA_DOMAIN}" if JIRA_DOMAIN else ""

# Output file
OUTPUT_FILE = DOCS_DIR / f"jira_backlog_{JIRA_PROJECT}.md"


def convert_jira_table_block(text: str) -> str:
    """
    Convert simple Jira wiki table blocks into Markdown tables.
    """
    lines = text.splitlines()
    converted: list[str] = []
    in_table = False
    header_done = False

    for line in lines:
        stripped = line.strip().replace(r"\|", "|")

        is_jira_header = stripped.startswith("||") and stripped.endswith("||")
        is_jira_row = stripped.startswith("|") and stripped.endswith("|")

        if is_jira_header or is_jira_row:
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            cells = [cell for cell in cells if cell]

            if cells:
                converted.append("| " + " | ".join(cells) + " |")

                if not header_done:
                    converted.append("| " + " | ".join(["---"] * len(cells)) + " |")
                    header_done = True

                in_table = True
                continue

        if in_table:
            in_table = False
            header_done = False

        converted.append(line)

    return "\n".join(converted)


def safe_markdown(text: str | None) -> str:
    """
    Normalize Jira text into Markdown-friendly output.
    """
    if not text:
        return "_No content_"

    cleaned = text.strip()
    cleaned = cleaned.replace(r"\|", "|")

    cleaned = re.sub(r"(?m)^h1\.\s+", "# ", cleaned)
    cleaned = re.sub(r"(?m)^h2\.\s+", "## ", cleaned)
    cleaned = re.sub(r"(?m)^h3\.\s+", "### ", cleaned)
    cleaned = re.sub(r"(?m)^h4\.\s+", "#### ", cleaned)

    cleaned = cleaned.replace("{{", "`").replace("}}", "`")
    cleaned = convert_jira_table_block(cleaned)

    return cleaned


def format_date(date_str: str | None) -> str:
    """
    Convert Jira datetime string into YYYY-MM-DD.
    """
    if not date_str:
        return "N/A"
    return date_str.split("T")[0]


def connect_to_jira() -> JIRA | None:
    """
    Create Jira client connection.
    """
    try:
        print(f"Connecting to Jira: {JIRA_URL}")
        jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))
        user = jira.myself()
        display_name = user.get("displayName", "Unknown User")
        print(f"Connected as: {display_name}\n")
        return jira
    except Exception as exc:
        print(f"Error connecting to Jira: {exc}")
        return None


def get_sprint_field_id(jira: JIRA) -> str | None:
    """
    Discover the Jira custom field ID used for Sprint.
    """
    try:
        for field in jira.fields():
            if field.get("name") == "Sprint":
                return field.get("id")
    except Exception as exc:
        print(f"Warning: Could not resolve Sprint field: {exc}")
    return None


def extract_sprint_name(issue: Any, sprint_field_id: str | None) -> str:
    """
    Extract sprint name from issue.
    """
    if not sprint_field_id:
        return "No Sprint"

    sprint_value = getattr(issue.fields, sprint_field_id, None)
    if not sprint_value:
        return "No Sprint"

    if isinstance(sprint_value, list):
        latest = sprint_value[-1]

        if hasattr(latest, "name"):
            return latest.name

        latest_str = str(latest)
        if "name=" in latest_str:
            try:
                return latest_str.split("name=")[1].split(",")[0]
            except IndexError:
                return "No Sprint"

        return latest_str

    if hasattr(sprint_value, "name"):
        return sprint_value.name

    return str(sprint_value)


def extract_description(issue: Any) -> str:
    """
    Extract issue description safely.
    """
    description = getattr(issue.fields, "description", None)
    return safe_markdown(description)


def extract_comments(issue: Any) -> list[str]:
    """
    Extract issue comments in readable Markdown format.
    """
    comment_block = getattr(issue.fields, "comment", None)
    if not comment_block or not getattr(comment_block, "comments", None):
        return []

    comments: list[str] = []
    for comment in comment_block.comments:
        author = getattr(comment.author, "displayName", "Unknown")
        created = format_date(getattr(comment, "created", None))
        body = safe_markdown(getattr(comment, "body", None))
        comments.append(f"- **{author}** ({created}): {body}")
    return comments


def fetch_jira_issues(jira: JIRA) -> list[Any]:
    """
    Fetch all project issues from Jira.
    """
    jql = f"project={JIRA_PROJECT} ORDER BY created DESC"
    print(f"Fetching issues from project {JIRA_PROJECT}...")
    print(f"Using JQL: {jql}\n")

    issues = jira.search_issues(jql, maxResults=False)
    print(f"Found {len(issues)} issues in project {JIRA_PROJECT}\n")
    return issues


def group_issues_by_status(issues: list[Any]) -> dict[str, list[Any]]:
    """
    Group issues by Jira status category.
    """
    status_groups: dict[str, list[Any]] = {
        "To Do": [],
        "In Progress": [],
        "Done": [],
    }

    for issue in issues:
        category = getattr(issue.fields.status.statusCategory, "name", "To Do")
        if category in status_groups:
            status_groups[category].append(issue)
        else:
            status_groups["To Do"].append(issue)

    return status_groups


def export_to_markdown(jira: JIRA, issues: list[Any]) -> None:
    """
    Export Jira issues to Markdown.
    """
    sprint_field_id = get_sprint_field_id(jira)
    status_groups = group_issues_by_status(issues)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        file.write(f"# Jira Backlog for Project {JIRA_PROJECT}\n")
        file.write(f"_Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
        file.write(f"**Total Issues:** {len(issues)}\n\n")

        file.write("## Summary\n\n")
        for status_name, status_issues in status_groups.items():
            file.write(f"- **{status_name}:** {len(status_issues)} issues\n")
        file.write("\n---\n\n")

        for status_name, status_issues in status_groups.items():
            if not status_issues:
                continue

            file.write(f"## {status_name} ({len(status_issues)} issues)\n\n")
            file.write("| Key | Summary | Status | Created | Updated | Sprint |\n")
            file.write("|-----|---------|--------|---------|---------|--------|\n")

            for issue in status_issues:
                key = issue.key
                summary = safe_markdown(issue.fields.summary)
                status = issue.fields.status.name
                created = format_date(issue.fields.created)
                updated = format_date(issue.fields.updated)
                sprint = safe_markdown(extract_sprint_name(issue, sprint_field_id))

                file.write(
                    f"| {key} | {summary} | {status} | {created} | {updated} | {sprint} |\n"
                )

            file.write("\n")

            for issue in status_issues:
                key = issue.key
                summary = safe_markdown(issue.fields.summary)
                status = issue.fields.status.name
                created = format_date(issue.fields.created)
                updated = format_date(issue.fields.updated)
                sprint = safe_markdown(extract_sprint_name(issue, sprint_field_id))
                description = extract_description(issue)
                comments = extract_comments(issue)

                file.write(f"### {key} – {summary}\n\n")
                file.write(f"- **Status:** {status}\n")
                file.write(f"- **Created:** {created}\n")
                file.write(f"- **Updated:** {updated}\n")
                file.write(f"- **Sprint:** {sprint}\n\n")

                file.write("**Description**\n\n")
                file.write(f"{description}\n\n")

                file.write("**Comments**\n\n")
                if comments:
                    for comment in comments:
                        file.write(f"{comment}\n")
                else:
                    file.write("_No comments_\n")

                file.write("\n---\n\n")

    print(f"Exported {len(issues)} issues to {OUTPUT_FILE}")


def validate_env() -> None:
    """
    Validate required environment variables.
    """
    if not JIRA_EMAIL or not JIRA_TOKEN:
        print("Error: JIRA_EMAIL and JIRA_TOKEN are required in .env")
        raise SystemExit(1)

    if not JIRA_DOMAIN:
        print("Error: JIRA_DOMAIN is required in .env")
        raise SystemExit(1)


if __name__ == "__main__":
    validate_env()

    print(f"Using Jira URL: {JIRA_URL}")
    print(f"Using Jira Project: {JIRA_PROJECT}\n")

    jira_client = connect_to_jira()
    if not jira_client:
        raise SystemExit(1)

    issues = fetch_jira_issues(jira_client)

    if issues:
        export_to_markdown(jira_client, issues)
        print(f"\nSuccess! Backlog exported to {OUTPUT_FILE}")
    else:
        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            file.write(f"# Jira Backlog for Project {JIRA_PROJECT}\n")
            file.write(f"_Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
            file.write("**No issues found.**\n\n")

        print(f"\nNo issues found in project {JIRA_PROJECT}")
        print(f"Created empty backlog file: {OUTPUT_FILE}")