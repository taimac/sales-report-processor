from __future__ import annotations

import csv
from pathlib import Path

from reports.services.dashboard_service import format_quantity, parse_decimal


def _format_quantity_field(value: str | None) -> str:
    """
    Normalize quantity-like report fields into Brazilian thousand-grouped text.
    """
    raw = (value or "").strip()
    if not raw:
        return ""
    return format_quantity(parse_decimal(raw))


def _build_csv_row(customer: dict, item: dict, continuation: dict | None = None) -> dict:
    """
    Build a flat CSV row for either a main item or one of its continuation rows.

    Continuation rows reuse the parent item's identity/commercial fields so the
    exported CSV preserves structure for comparison, while overriding the
    continuation-specific operational fields.
    """
    row = {
        "representative": customer.get("representative", ""),
        "customer_name": customer.get("customer_name", ""),
        "est": item.get("est", ""),
        "pedido": item.get("pedido", ""),
        "seq": item.get("seq", ""),
        "descricao": item.get("descricao", ""),
        "espess": item.get("espess", ""),
        "larg": item.get("larg", ""),
        "compr": item.get("compr", ""),
        "ord_prod": item.get("ord_prod", ""),
        "sit_ordem": item.get("sit_ordem", ""),
        "dt_entr": item.get("dt_entr", ""),
        "aa": item.get("aa", ""),
        "qt_ped": _format_quantity_field(item.get("qt_ped", "")),
        "qt_pc": _format_quantity_field(item.get("qt_pc", "")),
        "qt_prod": _format_quantity_field(item.get("qt_prod", "")),
        "qt_fatur": _format_quantity_field(item.get("qt_fatur", "")),
        "sdo_estoq": _format_quantity_field(item.get("sdo_estoq", "")),
        "sit": item.get("sit", ""),
        "pre_liq": item.get("pre_liq", ""),
        "pf": item.get("pf", ""),
        "vlr_peca": item.get("vlr_peca", ""),
        "pag": item.get("pag", ""),
        "transp": item.get("transp", ""),
        "cr_pro": item.get("cr_pro", ""),
        "cr_fat": item.get("cr_fat", ""),
        "o_compra": item.get("o_compra", ""),
        "item_cli": item.get("item_cli", ""),
        "mnf": item.get("mnf", ""),
        "raw_line": item.get("raw_line", ""),
    }

    if continuation is not None:
        row["ord_prod"] = continuation.get("ord_prod", "")
        row["sit_ordem"] = continuation.get("sit_ordem", "")
        row["qt_prod"] = _format_quantity_field(continuation.get("qt_prod", ""))
        row["sit"] = continuation.get("sit", "")
        row["raw_line"] = continuation.get("raw_line", "")

    return row


def export_report_to_csv(report: dict, output_path: str | Path) -> None:
    """
    Export an already parsed SRP report to CSV.
    One row per main item, plus one row per continuation row.
    """
    headers = [
        "representative",
        "customer_name",
        "est",
        "pedido",
        "seq",
        "descricao",
        "espess",
        "larg",
        "compr",
        "ord_prod",
        "sit_ordem",
        "dt_entr",
        "aa",
        "qt_ped",
        "qt_pc",
        "qt_prod",
        "qt_fatur",
        "sdo_estoq",
        "sit",
        "pre_liq",
        "pf",
        "vlr_peca",
        "pag",
        "transp",
        "cr_pro",
        "cr_fat",
        "o_compra",
        "item_cli",
        "mnf",
        "raw_line",
    ]

    output_path = Path(output_path)

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=";")
        writer.writeheader()

        for customer in report["customers"]:
            for item in customer["items"]:
                writer.writerow(_build_csv_row(customer, item))

                for continuation in item.get("continuations", []):
                    writer.writerow(_build_csv_row(customer, item, continuation))
