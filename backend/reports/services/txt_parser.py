from __future__ import annotations

from pathlib import Path
import re
from typing import Any, List, Dict



TIMESTAMP_PATTERN = re.compile(
    r"(?P<date>\d{2}/\d{2}/\d{4})\s*-\s*(?P<time>\d{2}:\d{2}:\d{2})"
)

MAIN_ROW_PATTERN = re.compile(r"^\s*\d+\s+\d+\s+\d+\s+")

CONTINUATION_PATTERN = re.compile(r"^\s{10,}\d[\d\.\sA-Z]*")

MAIN_ROW_LEADING_PATTERN = re.compile(
    r"^\s*(?P<est>\d+)\s+(?P<pedido>\d+)\s+(?P<seq>\d+)\s+"
)

THICKNESS_PATTERN = re.compile(r"\d+,\d{2}")

KNOWN_MULTIWORD_STATUSES = (
    "Em Produ",
    "Fat Parc",
    "OP Cancel",
    "Sem MP",
)

KNOWN_SINGLEWORD_STATUSES = {
    "Em",
    "Fat",
    "OP",
    "Produzido",
    "Pendente",
    "Aguardando",
}



def read_txt_report(file_path: str | Path) -> dict[str, Any]:
    """
    Read a TXT report safely, normalize line endings, preserve raw text,
    and extract generated date/time metadata.
    """
    path = Path(file_path)
    raw_bytes = path.read_bytes()

    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw_text = raw_bytes.decode("latin-1")

    normalized_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.replace("\x0c", "").rstrip() for line in normalized_text.split("\n")]

    metadata = extract_generated_datetime(lines)

    return {
        "raw_text": raw_text,
        "lines": lines,
        "metadata": metadata,
    }


def extract_generated_datetime(lines: list[str]) -> dict[str, str | None]:
    """
    Extract report generated date and time from the header area.
    Returns None values if not found.
    """
    for line in lines:
        match = TIMESTAMP_PATTERN.search(line)
        if match:
            return {
                "generated_date": match.group("date"),
                "generated_time": match.group("time"),
            }

    return {
        "generated_date": None,
        "generated_time": None,
    }

def is_blank(line: str) -> bool:
    return line.strip() == ""


def is_separator_line(line: str) -> bool:
    stripped = line.strip()
    return (
        len(stripped) > 10
        and (set(stripped) <= {"-", "="} or stripped.startswith("---"))
    )


def is_customer_header_line(line: str) -> bool:
    return "Rep:" in line and "Cliente:" in line


def is_table_header_line(line: str) -> bool:
    return "Est Pedido" in line and "Descrição" in line


def is_client_total_line(line: str) -> bool:
    return "TOT CLIENTE:" in line


def is_client_currency_total_line(line: str) -> bool:
    return "TOTAL CLIENTE EM R$:" in line


def is_grand_total_line(line: str) -> bool:
    return "TOTAL GERAL:" in line


def is_grand_currency_total_line(line: str) -> bool:
    return "TOTAL EM R$:" in line


def is_main_detail_row(line: str) -> bool:
    return bool(MAIN_ROW_PATTERN.match(line))


def is_continuation_row(line: str) -> bool:
    # continuation rows are indented and contain order references/status
    return (
        not is_main_detail_row(line)
        and bool(CONTINUATION_PATTERN.match(line))
    )


def classify_line(line: str) -> str:
    if is_blank(line):
        return "blank"
    if is_separator_line(line):
        return "separator"
    if is_customer_header_line(line):
        return "customer_header"
    if is_table_header_line(line):
        return "table_header"
    if is_client_total_line(line):
        return "client_total"
    if is_client_currency_total_line(line):
        return "client_total_currency"
    if is_grand_total_line(line):
        return "grand_total"
    if is_grand_currency_total_line(line):
        return "grand_total_currency"
    if is_continuation_row(line):
        return "continuation"
    if is_main_detail_row(line):
        return "main_detail"

    return "ignorable"


def classify_report_lines(lines: List[str]) -> List[Dict[str, str]]:
    return [{"line": line, "type": classify_line(line)} for line in lines]


def parse_customer_header(line: str) -> Dict[str, str]:
    # Example: "Rep: MACIEL       Cliente: FLANTECH"
    rep_match = re.search(r"Rep:\s*(\S+)", line)
    client_match = re.search(r"Cliente:\s*(.+)", line)

    return {
        "representative": rep_match.group(1) if rep_match else "",
        "customer_name": client_match.group(1).strip() if client_match else "",
    }


def detect_customer_blocks(lines: List[str]) -> List[Dict[str, Any]]:
    blocks = []
    current_block = None

    for line in lines:
        line_type = classify_line(line)

        if line_type == "customer_header":
            if current_block:
                blocks.append(current_block)

            header_data = parse_customer_header(line)

            current_block = {
                "header_line": line,
                "representative": header_data["representative"],
                "customer_name": header_data["customer_name"],
                "lines": [],
            }
            continue

        if current_block:
            current_block["lines"].append(
                {"line": line, "type": line_type}
            )

    if current_block:
        blocks.append(current_block)

    return blocks

def parse_main_row_identity_fields(line: str) -> dict[str, str]:
    """
    Parse the SRP-23 identity/product columns from a fixed-width main detail row.

    Fields:
    - est
    - pedido
    - seq
    - descricao
    - espess
    - larg
    - compr
    """
    if classify_line(line) != "main_detail":
        return {
            "raw_line": line,
            "est": "",
            "pedido": "",
            "seq": "",
            "descricao": "",
            "espess": "",
            "larg": "",
            "compr": "",
        }

    leading_match = MAIN_ROW_LEADING_PATTERN.match(line)
    seq = leading_match.group("seq") if leading_match else line[15:17].strip()

    return {
        "raw_line": line,
        "est": line[0:2].strip(),
        "pedido": line[4:10].strip(),
        "seq": seq,
        "descricao": line[18:56].strip(),
        "espess": line[59:63].strip(),
        "larg": line[64:72].strip(),
        "compr": line[84:88].strip(),
    }


def parse_main_detail_lines(lines: list[str]) -> list[dict[str, str]]:
    """
    Parse all lines classified as main_detail and return only SRP-23 fields.
    """
    parsed_rows: list[dict[str, str]] = []

    for line in lines:
        if classify_line(line) == "main_detail":
            parsed_rows.append(parse_main_row_identity_fields(line))

    return parsed_rows

def _extract_primary_status(raw_status: str) -> str:
    """
    Extract the canonical item status from a possibly over-captured status field.

    The TXT rows can leak extra columns into the status area. We normalize at
    parse time so only the real status reaches persistence.
    """
    if not raw_status or not raw_status.strip():
        return ""

    cleaned_status = raw_status.strip()

    for candidate in KNOWN_MULTIWORD_STATUSES:
        if cleaned_status.startswith(candidate):
            return candidate

    first_token = cleaned_status.split()[0]
    if first_token in KNOWN_SINGLEWORD_STATUSES:
        return first_token

    return first_token


def _is_credit_token(token: str) -> bool:
    return token.strip().lower() in {"sim", "nao", "não"}


def parse_main_row_operational_fields(line: str) -> dict[str, str]:
    """
    Parse SRP-18 operational and quantity columns from a main detail row.

    Strategy:
    - SRP-23 already parsed up to `compr`
    - from the remainder, use whitespace tokenization because numeric widths vary
    - NEW: Clean the `sit` field to extract only the primary status token
    """
    if classify_line(line) != "main_detail":
        return {}

    remainder = line[88:].strip()
    parts = remainder.split()

    # Expected order in the remainder:
    # ord_prod(optional), sit_ordem(optional like LC10), dt_entr, aa,
    # qt_ped, qt_pc, qt_prod, qt_fatur, sdo_estoq, sit...
    #
    # In some rows, sit_ordem is blank.
    # We detect date first, then infer what comes before it.

    date_index = next(
        (i for i, part in enumerate(parts) if re.fullmatch(r"\d{2}/\d{2}/\d{2}", part)),
        None,
    )

    if date_index is None:
        return {
            "ord_prod": "",
            "sit_ordem": "",
            "dt_entr": "",
            "aa": "",
            "qt_ped": "",
            "qt_pc": "",
            "qt_prod": "",
            "qt_fatur": "",
            "sdo_estoq": "",
            "sit": "",
        }

    pre_date_parts = parts[:date_index]

    if not pre_date_parts:
        ord_prod = ""
        sit_ordem = ""
    elif re.fullmatch(r"\d[\d\.]*", pre_date_parts[0]):
        ord_prod = pre_date_parts[0]
        sit_ordem = " ".join(pre_date_parts[1:])
    else:
        # Some rows omit the production order entirely but may still carry
        # order-status tokens before the delivery date.
        ord_prod = ""
        sit_ordem = " ".join(pre_date_parts)

    dt_entr = parts[date_index]
    aa = parts[date_index + 1] if len(parts) > date_index + 1 else ""
    qt_ped = parts[date_index + 2] if len(parts) > date_index + 2 else ""
    qt_pc = parts[date_index + 3] if len(parts) > date_index + 3 else ""
    qt_prod = parts[date_index + 4] if len(parts) > date_index + 4 else ""
    qt_fatur = parts[date_index + 5] if len(parts) > date_index + 5 else ""
    sdo_estoq = parts[date_index + 6] if len(parts) > date_index + 6 else ""
    
    tail_start = date_index + 7

    price_index = next(
        (
            i for i in range(tail_start, len(parts))
            if re.fullmatch(r"\d+,\d{3}", parts[i])
        ),
        None,
    )

    if price_index is None:
        raw_sit = " ".join(parts[tail_start:]) if len(parts) > tail_start else ""
    else:
        raw_sit = " ".join(parts[tail_start:price_index])

    # CRITICAL FIX: Extract only the primary status token at parse time
    sit = _extract_primary_status(raw_sit)

    return {
        "ord_prod": ord_prod,
        "sit_ordem": sit_ordem,
        "dt_entr": dt_entr,
        "aa": aa,
        "qt_ped": qt_ped,
        "qt_pc": qt_pc,
        "qt_prod": qt_prod,
        "qt_fatur": qt_fatur,
        "sdo_estoq": sdo_estoq,
        "sit": sit,  # ← Now clean: "Fat" instead of "Fat Parc 9,290 0,000 ..."
    }

def parse_main_row_full_step_1(line: str) -> dict[str, str]:
    """
    Combine SRP-23 and SRP-18 parsing (identity + operational).
    """

    base = parse_main_row_identity_fields(line)
    operational = parse_main_row_operational_fields(line)

    return {
        **base,
        **operational,
    }

def parse_main_detail_lines_step_1(lines: list[str]) -> list[dict[str, str]]:
    results = []

    for line in lines:
        if classify_line(line) == "main_detail":
            results.append(parse_main_row_full_step_1(line))

    return results

def parse_main_row_commercial_fields(line: str) -> dict[str, str]:
    """
    Parse SRP-19 commercial and reference fields from the row tail.

    Strategy:
    - work from the remainder after `compr`
    - anchor on the date token
    - find the first price token (`pre_liq`)
    - support rows where `pf` is blank
    """
    empty_result = {
        "pre_liq": "",
        "pf": "",
        "vlr_peca": "",
        "pag": "",
        "transp": "",
        "cr_pro": "",
        "cr_fat": "",
        "o_compra": "",
        "item_cli": "",
        "mnf": "",
    }

    if classify_line(line) != "main_detail":
        return empty_result

    remainder = line[88:].strip()
    parts = remainder.split()

    date_index = next(
        (i for i, part in enumerate(parts) if re.fullmatch(r"\d{2}/\d{2}/\d{2}", part)),
        None,
    )
    if date_index is None:
        return empty_result

    # After date:
    # aa, qt_ped, qt_pc, qt_prod, qt_fatur, sdo_estoq, sit..., pre_liq, ...
    tail_start = date_index + 7

    price_index = next(
        (
            i
            for i in range(tail_start, len(parts))
            if re.fullmatch(r"\d+,\d{3}", parts[i])
        ),
        None,
    )
    if price_index is None:
        return empty_result

    commercial_parts = parts[price_index:]

    pre_liq = commercial_parts[0] if len(commercial_parts) > 0 else ""

    def is_numeric_token(token: str) -> bool:
        return bool(re.fullmatch(r"\d+(?:\.\d+)*", token))

    pf = ""
    vlr_peca = ""
    pag = ""
    transp = ""
    cr_pro = ""
    cr_fat = ""
    o_compra = ""
    item_cli = ""
    mnf = ""

    tail = commercial_parts[1:]
    pag_index = next((i for i, token in enumerate(tail) if is_numeric_token(token)), None)
    if pag_index is None:
        return {
            "pre_liq": pre_liq,
            "pf": "",
            "vlr_peca": "",
            "pag": "",
            "transp": "",
            "cr_pro": "",
            "cr_fat": "",
            "o_compra": "",
            "item_cli": "",
            "mnf": "",
        }

    pre_pag = tail[:pag_index]
    if len(pre_pag) >= 1:
        pf = pre_pag[0]
    if len(pre_pag) >= 2:
        vlr_peca = pre_pag[1]
    pag = tail[pag_index]

    credit_index = next(
        (i for i in range(pag_index + 1, len(tail)) if _is_credit_token(tail[i])),
        None,
    )
    if credit_index is None:
        transp = " ".join(tail[pag_index + 1:]).strip()
        return {
            "pre_liq": pre_liq,
            "pf": pf,
            "vlr_peca": vlr_peca,
            "pag": pag,
            "transp": transp,
            "cr_pro": "",
            "cr_fat": "",
            "o_compra": "",
            "item_cli": "",
            "mnf": "",
        }

    transp = " ".join(tail[pag_index + 1:credit_index]).strip()
    cr_pro = tail[credit_index] if credit_index < len(tail) else ""
    cr_fat = tail[credit_index + 1] if credit_index + 1 < len(tail) else ""

    refs = [token for token in tail[credit_index + 2:] if token]

    if len(refs) == 1:
        o_compra = refs[0]
    elif len(refs) == 2:
        first_is_numeric = refs[0].isdigit()
        second_is_numeric = refs[1].isdigit()

        if first_is_numeric and second_is_numeric:
            if len(refs[1]) <= 2:
                item_cli = refs[0]
                mnf = refs[1]
            else:
                o_compra = refs[0]
                item_cli = refs[1]
        elif not first_is_numeric and not second_is_numeric:
            o_compra = " ".join(refs)
        else:
            o_compra = refs[0]
            item_cli = refs[1]
    elif len(refs) >= 3:
        o_compra = refs[0]
        item_cli = refs[1]
        mnf = refs[2]

    return {
        "pre_liq": pre_liq,
        "pf": pf,
        "vlr_peca": vlr_peca,
        "pag": pag,
        "transp": transp,
        "cr_pro": cr_pro,
        "cr_fat": cr_fat,
        "o_compra": o_compra,
        "item_cli": item_cli,
        "mnf": mnf,
    }

def parse_main_row_full(line: str) -> dict[str, str]:
    return {
        **parse_main_row_identity_fields(line),
        **parse_main_row_operational_fields(line),
        **parse_main_row_commercial_fields(line),
    }

def parse_main_detail_lines_full(lines: list[str]) -> list[dict[str, str]]:
    results = []

    for line in lines:
        if classify_line(line) == "main_detail":
            results.append(parse_main_row_full(line))

    return results

def parse_continuation_row(line: str) -> dict[str, str]:
    parts = line.strip().split()

    empty = {
        "raw_line": line,
        "ord_prod": "",
        "sit_ordem": "",
        "qt_prod": "",
        "sit": "",
    }

    if not parts:
        return empty

    ord_prod = parts[0]

    # Status is usually the trailing text after the last numeric quantity token
    last_numeric_index = None
    for i in range(len(parts) - 1, 0, -1):
        token = parts[i]
        if any(ch.isdigit() for ch in token):
            last_numeric_index = i
            break

    if last_numeric_index is None:
        return {
            **empty,
            "ord_prod": ord_prod,
            "sit": " ".join(parts[1:]).strip(),
        }

    qt_prod = parts[last_numeric_index]
    sit = " ".join(parts[last_numeric_index + 1:]).strip()
    sit_ordem = " ".join(parts[1:last_numeric_index - 1]).strip() if last_numeric_index > 2 else ""

    return {
        "raw_line": line,
        "ord_prod": ord_prod,
        "sit_ordem": sit_ordem,
        "qt_prod": qt_prod,
        "sit": sit,
    }

def attach_continuation_rows(lines: list[str]) -> list[dict]:
    """
    Attach continuation rows to their corresponding main rows.
    """
    results: list[dict] = []
    current_parent: dict | None = None

    for line in lines:
        line_type = classify_line(line)

        if line_type == "main_detail":
            current_parent = parse_main_row_full(line)
            current_parent["continuations"] = []
            results.append(current_parent)

        elif line_type == "continuation" and current_parent is not None:
            current_parent["continuations"].append(parse_continuation_row(line))

    return results

def extract_numeric_values(line: str) -> list[str]:
    """
    Extract numeric values like:
    1.234,56 or 123 or 12.000
    """
    return re.findall(r"\d[\d\.\,]*", line)


def parse_client_total_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_ped": values[0] if len(values) > 0 else "",
        "total_in_prod": values[1] if len(values) > 1 else "",
        "total_fatur": values[2] if len(values) > 2 else "",
        "total_sdo": values[3] if len(values) > 3 else "",
    }

def parse_client_total_currency_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_valor": values[0] if values else "",
    }

def parse_grand_total_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_ped": values[0] if len(values) > 0 else "",
        "total_in_prod": values[1] if len(values) > 1 else "",
        "total_fatur": values[2] if len(values) > 2 else "",
        "total_sdo": values[3] if len(values) > 3 else "",
    }

def parse_grand_total_currency_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_valor": values[0] if values else "",
    }

def extract_totals(lines: list[str]) -> dict[str, list[dict]]:
    client_totals = []
    grand_totals = []

    current_client_total = None

    for line in lines:
        line_type = classify_line(line)

        if line_type == "client_total":
            current_client_total = parse_client_total_line(line)

        elif line_type == "client_total_currency":
            if current_client_total:
                current_client_total.update(
                    parse_client_total_currency_line(line)
                )
                client_totals.append(current_client_total)
                current_client_total = None

        elif line_type == "grand_total":
            grand_totals.append(parse_grand_total_line(line))

        elif line_type == "grand_total_currency":
            if grand_totals:
                grand_totals[-1].update(
                    parse_grand_total_currency_line(line)
                )

    return {
        "client_totals": client_totals,
        "grand_totals": grand_totals,
    }

def assemble_report(file_path: str) -> dict:
    """
    Final SRP-22 assembly.
    """

    data = read_txt_report(file_path)
    lines = data["lines"]

    # Step 1 — detect customer blocks
    blocks = detect_customer_blocks(lines)

    customers = []

    for block in blocks:
        block_lines = [entry["line"] for entry in block["lines"]]

        # Step 2 — parse rows with continuations
        items = attach_continuation_rows(block_lines)

        # Step 3 — extract totals for this block
        block_totals = extract_totals(block_lines)

        customers.append({
            "representative": block["representative"],
            "customer_name": block["customer_name"],
            "items": items,
            "totals": block_totals,
        })

    # Step 4 — report-level totals
    # Only grand totals belong to the full report payload.
    report_totals = extract_totals(lines)
    totals = {
        "grand_totals": report_totals.get("grand_totals", []),
    }

    return {
        "metadata": data["metadata"],
        "customers": customers,
        "totals": totals,
    }
