"""
Purpose: Build decision-oriented dashboard data from persisted parsed reports.
Date: 2026-04-13
Author: Codex
Domain: Systems / SRP
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

from reports.services.txt_parser import assemble_report


BUCKET_CONFIG = [
    (
        "delivery_attention",
        "Entrega em Atencao",
        "Itens com entrega vencida, proxima ou sem previsao clara enquanto ainda estao em aberto.",
    ),
    (
        "credit_block",
        "Bloqueio de Credito",
        "Itens com restricao em CR PRO ou CR FAT e que precisam de acao comercial imediata.",
    ),
    (
        "production_follow_up",
        "Acompanhar Producao",
        "Itens ja em producao, mas ainda sem fechamento comercial adequado.",
    ),
    (
        "missing_production_reference",
        "Sem Ordem de Producao",
        "Itens em aberto que ainda nao possuem referencia operacional suficiente.",
    ),
    (
        "high_value_customer",
        "Cliente de Alto Valor",
        "Clientes com maior valor em aberto dentro do relatorio atual.",
    ),
    (
        "stock_balance",
        "Saldo em Estoque",
        "Itens que seguem com volume pendente e exigem acompanhamento comercial.",
    ),
]

PRIMARY_BUCKET_ORDER = [key for key, _, _ in BUCKET_CONFIG]
BUCKET_LABELS = {key: label for key, label, _ in BUCKET_CONFIG}
BUCKET_DESCRIPTIONS = {key: description for key, _, description in BUCKET_CONFIG}
BUCKET_WEIGHTS = {
    "delivery_attention": 100,
    "credit_block": 90,
    "production_follow_up": 80,
    "missing_production_reference": 70,
    "high_value_customer": 60,
    "stock_balance": 50,
}


def parse_decimal(value: str | None) -> Decimal:
    """
    Parse report-style numeric strings into Decimal safely.

    Invalid or blank values are treated as zero so the dashboard remains
    resilient when optional fields are missing or malformed.
    """
    raw = (value or "").strip()
    if not raw:
        return Decimal("0")

    if "." in raw and "," in raw:
        normalized = raw.replace(".", "").replace(",", ".")
    elif "," in raw:
        normalized = raw.replace(",", ".")
    elif "." in raw:
        integer_part, fractional_part = raw.split(".", 1)
        if integer_part.isdigit() and fractional_part.isdigit():
            normalized = integer_part + fractional_part.ljust(3, "0")
        else:
            normalized = raw.replace(".", "")
    else:
        if raw.isdigit() and len(raw) <= 2:
            normalized = f"{raw}000"
        else:
            normalized = raw

    try:
        return Decimal(normalized)
    except InvalidOperation:
        return Decimal("0")


def parse_report_date(raw_date: str | None) -> date | None:
    """
    Parse delivery dates from report fields.
    """
    if not raw_date:
        return None

    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(raw_date, fmt).date()
        except ValueError:
            continue
    return None


def format_decimal(value: Decimal) -> str:
    """
    Format Decimal values into pt-BR style strings.
    """
    quantized = value.quantize(Decimal("0.001"))
    formatted = f"{quantized:,.3f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_quantity(value: Decimal) -> str:
    """
    Format quantity-like values using Brazilian thousand separators.

    Quantity fields are stored internally as whole-unit decimals after
    normalization, so display should stay compact:
    - 500 -> 500
    - 12000 -> 12.000
    - 8500 -> 8.500
    """
    integer_value = int(value)
    return f"{integer_value:,}".replace(",", ".")


def format_currency(value: Decimal) -> str:
    """
    Format monetary values with Brazilian separators for dashboard display.
    """
    quantized = value.quantize(Decimal("0.01"))
    formatted = f"{quantized:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def _calculate_average_price(total_value: str | None, total_ordered: str | None) -> str:
    """
    Calculate report-level average price from total value and ordered quantity.
    """
    ordered_quantity = parse_decimal(total_ordered)
    report_value = parse_decimal(total_value)
    if ordered_quantity <= 0:
        return "0,00"
    return format_currency(report_value / ordered_quantity)


def _calculate_average_price_from_items(
    customers_payload: list[dict],
    report_total: dict,
) -> str | None:
    """
    Prefer item-level pricing when persisted items fully represent the report.

    Some supplier files can carry stale or manually edited grand-total value
    lines even when line-item prices changed. When the item-level ordered total
    matches the report ordered total, we can safely derive a fresher weighted
    average directly from persisted items.
    """
    report_ordered = parse_decimal(report_total.get("total_ped"))
    if report_ordered <= 0:
        return None

    item_ordered = Decimal("0")
    item_value = Decimal("0")

    for customer in customers_payload:
        for item in customer["items"]:
            ordered_qty = parse_decimal(item.get("qt_ped"))
            item_ordered += ordered_qty
            item_value += ordered_qty * parse_decimal(item.get("pre_liq"))

    if item_ordered <= 0 or item_value <= 0:
        return None

    # Only trust item-derived pricing when the item set fully covers the report.
    if item_ordered != report_ordered:
        return None

    return format_currency(item_value / item_ordered)


def _is_production_signal(status_text: str | None) -> bool:
    """
    Detect whether a status text suggests production movement.
    """
    lowered = (status_text or "").lower()
    return "produ" in lowered or "lc" in lowered


def _build_report_meta(parsed_report, source: str) -> dict:
    uploaded_file = ""
    if parsed_report.uploaded_report and parsed_report.uploaded_report.file:
        uploaded_file = parsed_report.uploaded_report.file.name

    return {
        "report_id": parsed_report.id,
        "generated_date": parsed_report.generated_date,
        "generated_time": parsed_report.generated_time,
        "uploaded_file": uploaded_file,
        "source": source,
    }


def _is_credit_blocked(value: str | None) -> bool:
    """
    Treat explicit "Nao" values in CR PRO / CR FAT as a credit block.
    """
    lowered = (value or "").strip().lower()
    return lowered in {"nao", "não"}


def _join_unique_text(values: list[str]) -> str:
    """
    Join non-empty strings while preserving order and removing duplicates.
    """
    unique_values = []
    for value in values:
        cleaned = (value or "").strip()
        if cleaned and cleaned not in unique_values:
            unique_values.append(cleaned)
    return " - ".join(unique_values)


def _resolve_order_references(item_data: dict) -> str:
    """
    Surface all production-order references attached to the item.

    Some report rows are split across multiple production orders, with one
    order on the main row and additional orders on continuation rows.
    """
    values = [(item_data.get("ord_prod") or "").strip()]
    values.extend(
        (continuation.get("ord_prod") or "").strip()
        for continuation in item_data.get("continuations", [])
    )
    return _join_unique_text(values)


def _resolve_order_status(item_data: dict) -> str:
    """
    Surface order status from the main row and any continuation rows.
    """
    values = [(item_data.get("sit_ordem") or "").strip()]
    values.extend(
        (continuation.get("sit_ordem") or "").strip()
        for continuation in item_data.get("continuations", [])
    )
    return _join_unique_text(values)


def _resolve_item_status(item_data: dict) -> str:
    """
    Fall back to continuation status when the main item status is blank.
    """
    direct_status = (item_data.get("sit") or "").strip()
    if direct_status:
        return direct_status

    return _join_unique_text(
        [
            (continuation.get("sit") or "").strip()
            for continuation in item_data.get("continuations", [])
        ]
    )


def _build_parser_snapshot(parsed_report) -> dict | None:
    """
    Rebuild the latest report data from the original uploaded TXT when available.

    This is used as a safe display-layer fallback for legacy persisted records
    whose mapped dashboard fields may be incomplete or malformed.
    """
    uploaded = parsed_report.uploaded_report
    if not uploaded or not uploaded.file:
        return None

    file_path = Path(uploaded.file.path)
    if not file_path.exists():
        return None

    try:
        return assemble_report(str(file_path))
    except Exception:
        return None


def _normalize_from_parser(parsed_report, parser_snapshot: dict) -> tuple[list[dict], dict]:
    customers_payload = []

    for customer_index, customer_data in enumerate(parser_snapshot.get("customers", []), start=1):
        totals = (customer_data.get("totals") or {}).get("client_totals", [])
        total_data = totals[0] if totals else {}
        items = []

        for item_index, item_data in enumerate(customer_data.get("items", []), start=1):
            items.append(
                {
                    "item_id": f"parser-{customer_index}-{item_index}",
                    "pedido": item_data.get("pedido", ""),
                    "seq": item_data.get("seq", ""),
                    "description": item_data.get("descricao", ""),
                    "larg": item_data.get("larg", ""),
                    "ord_prod": item_data.get("ord_prod", ""),
                    "sit_ordem": item_data.get("sit_ordem", ""),
                    "sit": item_data.get("sit", ""),
                    "dt_entr": item_data.get("dt_entr", ""),
                    "qt_ped": item_data.get("qt_ped", ""),
                    "qt_prod": item_data.get("qt_prod", ""),
                    "qt_fatur": item_data.get("qt_fatur", ""),
                    "sdo_estoq": item_data.get("sdo_estoq", ""),
                    "pre_liq": item_data.get("pre_liq", ""),
                    "transp": item_data.get("transp", ""),
                    "cr_pro": item_data.get("cr_pro", ""),
                    "cr_fat": item_data.get("cr_fat", ""),
                    "o_compra": item_data.get("o_compra", ""),
                    "item_cli": item_data.get("item_cli", ""),
                    "continuations": item_data.get("continuations", []),
                }
            )

        customers_payload.append(
            {
                "customer_id": f"parser-{customer_index}",
                "representative": customer_data.get("representative", ""),
                "customer_name": customer_data.get("customer_name", ""),
                "total_ped": total_data.get("total_ped", ""),
                "total_in_prod": total_data.get("total_in_prod", ""),
                "total_fatur": total_data.get("total_fatur", ""),
                "total_sdo": total_data.get("total_sdo", ""),
                "total_valor": total_data.get("total_valor", ""),
                "items": items,
            }
        )

    report_totals = (parser_snapshot.get("totals") or {}).get("grand_totals", [])
    report_total = report_totals[0] if report_totals else {}

    return customers_payload, report_total


def _normalize_from_persistence(parsed_report) -> tuple[list[dict], dict]:
    customers_payload = []

    for customer in parsed_report.customers.all():
        total = getattr(customer, "total", None)
        items = []

        for item in customer.items.all():
            items.append(
                {
                    "item_id": item.id,
                    "pedido": item.pedido,
                    "seq": item.seq,
                    "description": item.descricao,
                    "larg": item.larg,
                    "ord_prod": item.ord_prod,
                    "sit_ordem": item.sit_ordem,
                    "sit": item.sit,
                    "dt_entr": item.dt_entr,
                    "qt_ped": item.qt_ped,
                    "qt_prod": item.qt_prod,
                    "qt_fatur": item.qt_fatur,
                    "sdo_estoq": item.sdo_estoq,
                    "pre_liq": item.pre_liq,
                    "transp": item.transp,
                    "cr_pro": item.cr_pro,
                    "cr_fat": item.cr_fat,
                    "o_compra": item.o_compra,
                    "item_cli": item.item_cli,
                    "continuations": [
                        {
                            "ord_prod": continuation.ord_prod,
                            "sit_ordem": continuation.sit_ordem,
                            "qt_prod": continuation.qt_prod,
                            "sit": continuation.sit,
                        }
                        for continuation in item.continuations.all()
                    ],
                }
            )

        customers_payload.append(
            {
                "customer_id": customer.id,
                "representative": customer.representative,
                "customer_name": customer.customer_name,
                "total_ped": total.total_ped if total else "",
                "total_in_prod": total.total_in_prod if total else "",
                "total_fatur": total.total_fatur if total else "",
                "total_sdo": total.total_sdo if total else "",
                "total_valor": total.total_valor if total else "",
                "items": items,
            }
        )

    report_total = getattr(parsed_report, "total", None)
    total_payload = {
        "total_ped": report_total.total_ped if report_total else "",
        "total_in_prod": report_total.total_in_prod if report_total else "",
        "total_fatur": report_total.total_fatur if report_total else "",
        "total_sdo": report_total.total_sdo if report_total else "",
        "total_valor": report_total.total_valor if report_total else "",
    }

    return customers_payload, total_payload


def _should_use_parser_snapshot(customers_payload: list[dict], report_total: dict) -> bool:
    has_blank_totals = not any(
        (report_total.get(field) or "").strip()
        for field in ("total_ped", "total_in_prod", "total_fatur", "total_sdo", "total_valor")
    )
    has_blank_customer_totals = any(
        not any((customer.get(field) or "").strip() for field in ("total_ped", "total_in_prod", "total_fatur", "total_sdo", "total_valor"))
        for customer in customers_payload
    )
    return has_blank_totals or has_blank_customer_totals


def _compute_summary_from_items(customers_payload: list[dict]) -> dict:
    total_ordered = Decimal("0")
    total_in_production = Decimal("0")
    total_invoiced = Decimal("0")
    total_open_balance = Decimal("0")

    for customer in customers_payload:
        for item in customer["items"]:
            total_ordered += parse_decimal(item.get("qt_ped"))
            total_in_production += parse_decimal(item.get("qt_prod"))
            total_invoiced += parse_decimal(item.get("qt_fatur"))
            total_open_balance += parse_decimal(item.get("sdo_estoq"))

    return {
        "total_ped": format_quantity(total_ordered),
        "total_in_prod": format_quantity(total_in_production),
        "total_fatur": format_quantity(total_invoiced),
        "total_sdo": format_quantity(total_open_balance),
        "total_valor": "",
    }


def _build_reason_text(signals: list[str]) -> str:
    return " + ".join(BUCKET_LABELS[signal] for signal in signals)


def _build_next_action(signals: list[str]) -> str:
    if "credit_block" in signals and "delivery_attention" in signals:
        return "Liberar credito e cobrar definicao de entrega"
    if "credit_block" in signals:
        return "Validar bloqueio com financeiro e cliente"
    if "missing_production_reference" in signals:
        return "Cobrar ordem de producao / MP"
    if "delivery_attention" in signals:
        return "Confirmar entrega e destravar pendencia"
    if "production_follow_up" in signals:
        return "Acompanhar producao e faturamento"
    if "stock_balance" in signals:
        return "Confirmar saldo e proxima expedicao"
    if "high_value_customer" in signals:
        return "Priorizar contato comercial"
    return "Analisar carteira"


def _build_deadline_label(signals: list[str], delivery_date: date | None, today: date) -> str:
    if delivery_date and delivery_date < today:
        return "Hoje"
    if "credit_block" in signals or "delivery_attention" in signals:
        return "Hoje"
    if "missing_production_reference" in signals:
        return "1 dia"
    if "production_follow_up" in signals:
        return "2 dias"
    return "3 dias"


def _build_priority_label(signals: list[str], delivery_date: date | None, today: date) -> str:
    if (delivery_date and delivery_date < today) or "credit_block" in signals or (
        "delivery_attention" in signals and "missing_production_reference" in signals
    ):
        return "Alta"
    if "delivery_attention" in signals or "production_follow_up" in signals:
        return "Media"
    return "Baixa"


def _compute_client_flag_map(action_items: list[dict], client_rows: list[dict], high_value_customer_ids: set) -> list[dict]:
    flags_by_client = defaultdict(set)
    for item in action_items:
        flags_by_client[item["customer_id"]].update(item["signals"])

    top_value_ids = [row["customer_id"] for row in sorted(client_rows, key=lambda row: row["open_value_decimal"], reverse=True) if row["open_value_decimal"] > 0]
    alto_ids = set(top_value_ids[:3])
    medio_ids = set(top_value_ids[3:5])

    matrix_rows = []
    for row in client_rows:
        signals = flags_by_client[row["customer_id"]]
        if row["customer_id"] in alto_ids:
            value_level = "Alto"
        elif row["customer_id"] in medio_ids:
            value_level = "Medio"
        else:
            value_level = "Baixo"

        matrix_rows.append(
            {
                "customer_id": row["customer_id"],
                "customer_name": row["customer_name"],
                "credit_block": "Sim" if "credit_block" in signals else "Nao",
                "production_follow_up": "Sim" if "production_follow_up" in signals else "Nao",
                "delivery_attention": "Sim" if "delivery_attention" in signals else "Nao",
                "stock_balance": "Sim" if "stock_balance" in signals else "Nao",
                "high_value_customer": value_level if row["customer_id"] in high_value_customer_ids else value_level,
            }
        )

    return matrix_rows


def _build_client_focus_reason(signal_key: str | None, row: dict) -> str:
    if signal_key == "credit_block":
        return "Cliente com bloqueio de credito em itens relevantes da carteira."
    if signal_key == "delivery_attention":
        return "Cliente concentra entregas vencidas ou proximas com demanda ainda em aberto."
    if signal_key == "missing_production_reference":
        return "Cliente possui itens sem referencia de producao suficiente para o prazo atual."
    if signal_key == "production_follow_up":
        return "Cliente exige acompanhamento de producao para garantir cobertura da entrega."
    if signal_key == "high_value_customer":
        return "Cliente concentra carteira aberta relevante e merece leitura prioritaria."
    return (
        "Cliente segue com carteira ativa em acompanhamento, mesmo sem um sinal dominante unico."
    )


def _build_client_next_reading(signal_key: str | None) -> str:
    if signal_key == "credit_block":
        return "Validar credito e destravar pedidos."
    if signal_key == "delivery_attention":
        return "Revisar itens vencidos e cobrar entrega."
    if signal_key == "missing_production_reference":
        return "Validar OP e programacao dos itens mais pressionados."
    if signal_key == "production_follow_up":
        return "Cobrar programacao e cobertura de producao."
    if signal_key == "high_value_customer":
        return "Abrir Cliente 360 e revisar exposicao da carteira."
    return "Abrir Cliente 360 para leitura completa da conta."


def _enrich_client_rows(
    client_rows: list[dict],
    action_items: list[dict],
) -> list[dict]:
    signal_counts_by_client = defaultdict(lambda: defaultdict(int))

    for item in action_items:
        for signal in item["signals"]:
            signal_counts_by_client[item["customer_id"]][signal] += 1

    enriched_rows = []
    for row in client_rows:
        signal_counts = signal_counts_by_client[row["customer_id"]]
        dominant_signal = None
        if signal_counts:
            dominant_signal = max(
                signal_counts.items(),
                key=lambda entry: (
                    BUCKET_WEIGHTS[entry[0]],
                    entry[1],
                ),
            )[0]

        enriched_row = {
            **row,
            "dominant_signal_key": dominant_signal,
            "dominant_signal_label": BUCKET_LABELS.get(
                dominant_signal,
                "Carteira em acompanhamento",
            ),
            "focus_reason": _build_client_focus_reason(dominant_signal, row),
            "next_reading": _build_client_next_reading(dominant_signal),
        }
        enriched_rows.append(enriched_row)

    enriched_rows.sort(
        key=lambda row: (
            row["action_priority"],
            row["action_flag_count"],
            row["open_value_decimal"],
            row["customer_name"],
        ),
        reverse=True,
    )
    return enriched_rows


def _build_rankings(client_rows: list[dict], action_items: list[dict], customers_payload: list[dict], today: date) -> dict:
    top_clients_by_value = [
        {
            "customer_name": row["customer_name"],
            "value": row["total_valor"] or "0",
        }
        for row in sorted(client_rows, key=lambda row: row["open_value_decimal"], reverse=True)[:5]
    ]

    top_clients_by_weight = [
        {
            "customer_name": row["customer_name"],
            "value": row["total_sdo"] or "0",
        }
        for row in sorted(client_rows, key=lambda row: parse_decimal(row["total_sdo"]), reverse=True)[:5]
    ]

    top_clients_by_actionable = [
        {
            "customer_name": row["customer_name"],
            "value": row["action_flag_count"],
        }
        for row in sorted(client_rows, key=lambda row: (row["action_flag_count"], row["action_priority"], row["open_value_decimal"]), reverse=True)[:5]
    ]

    order_stock = defaultdict(Decimal)
    order_overdue = defaultdict(Decimal)
    product_volume = defaultdict(Decimal)

    for item in action_items:
        order_stock[(item["customer_name"], item["pedido"])] += parse_decimal(item["sdo_estoq"])
        delivery_date = parse_report_date(item["dt_entr"])
        if delivery_date and delivery_date < today:
            order_overdue[(item["customer_name"], item["pedido"])] += parse_decimal(item["sdo_estoq"])
        product_volume[item["description"]] += parse_decimal(item["qt_ped"])

    top_orders_by_stock = [
        {"customer_name": customer_name, "pedido": pedido, "value": format_quantity(value)}
        for (customer_name, pedido), value in sorted(order_stock.items(), key=lambda entry: entry[1], reverse=True)[:5]
    ]
    top_orders_by_delay = [
        {"customer_name": customer_name, "pedido": pedido, "value": format_quantity(value)}
        for (customer_name, pedido), value in sorted(order_overdue.items(), key=lambda entry: entry[1], reverse=True)[:5]
    ]
    top_products_by_volume = [
        {"description": description, "value": format_quantity(value)}
        for description, value in sorted(product_volume.items(), key=lambda entry: entry[1], reverse=True)[:5]
        if description
    ]

    return {
        "top_clients_by_value": top_clients_by_value,
        "top_clients_by_weight": top_clients_by_weight,
        "top_clients_by_actionable": top_clients_by_actionable,
        "top_orders_by_stock": top_orders_by_stock,
        "top_orders_by_delay": top_orders_by_delay,
        "top_products_by_volume": top_products_by_volume,
    }


def _build_delivery_timeline(action_items: list[dict], generated_report_date: date | None, today: date) -> list[dict]:
    weeks = {}
    if generated_report_date:
        timeline_month = generated_report_date.month
        timeline_year = generated_report_date.year
    else:
        timeline_month = today.month
        timeline_year = today.year

    for item in action_items:
        delivery_date = parse_report_date(item["dt_entr"])
        if not delivery_date:
            continue
        if delivery_date.month != timeline_month or delivery_date.year != timeline_year:
            continue

        week_start = delivery_date - timedelta(days=delivery_date.weekday())
        week_end = week_start + timedelta(days=6)
        week_key = week_start.isoformat()
        if week_key not in weeks:
            weeks[week_key] = {
                "label": f"Semana {week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m')}",
                "total_weight": Decimal("0"),
                "clients": set(),
                "critical_count": 0,
                "days": defaultdict(list),
            }

        requested_minus_delivered = max(
            Decimal("0"),
            parse_decimal(item["qt_ped"]) - parse_decimal(item["qt_fatur"]),
        )
        weeks[week_key]["total_weight"] += requested_minus_delivered
        weeks[week_key]["clients"].add(item["customer_name"])
        if item["priority_label"] == "Alta":
            weeks[week_key]["critical_count"] += 1
        weeks[week_key]["days"][delivery_date.strftime("%d/%m")].append(item)

    timeline = []
    for week_key in sorted(weeks.keys()):
        week = weeks[week_key]
        timeline.append(
            {
                "label": week["label"],
                "total_weight": format_quantity(week["total_weight"]),
                "impacted_clients": len(week["clients"]),
                "critical_count": week["critical_count"],
                "days": [
                    {"label": day_label, "items": items}
                    for day_label, items in sorted(
                        week["days"].items(),
                        key=lambda entry: datetime.strptime(entry[0], "%d/%m"),
                    )
                ],
            }
        )

    return timeline[:4]


def _build_client_360(client_rows: list[dict], action_items: list[dict], matrix_rows: list[dict]) -> dict | None:
    if not client_rows:
        return None

    # `client_rows` is already ordered by business priority in `Carteira em Foco`,
    # so the drilldown should follow that first-ranked account explicitly.
    focus_client = client_rows[0]
    client_items = [item for item in action_items if item["customer_id"] == focus_client["customer_id"]]
    client_flags = next(
        (row for row in matrix_rows if row["customer_id"] == focus_client["customer_id"]),
        None,
    )

    return {
        "customer_name": focus_client["customer_name"],
        "representative": focus_client["representative"],
        "selected_from": "Carteira em Foco",
        "selection_rank": 1,
        "selection_reason": focus_client["focus_reason"],
        "selection_hint": focus_client["next_reading"],
        "dominant_signal_label": focus_client["dominant_signal_label"],
        "action_flag_count": focus_client["action_flag_count"],
        "action_priority": focus_client["action_priority"],
        "critical_item_count": len(client_items),
        "summary": {
            "portfolio_value": focus_client["total_valor"] or "0",
            "total_ordered": focus_client["total_ped"] or "0",
            "total_in_production": focus_client["total_in_prod"] or "0",
            "total_invoiced": focus_client["total_fatur"] or "0",
            "open_balance": focus_client["total_sdo"] or "0",
        },
        "flags": [
            label
            for key, label, _ in BUCKET_CONFIG
            if client_flags and client_flags.get(key) == "Sim"
        ],
        "items": client_items,
    }


def _build_credit_blocked_orders(action_items: list[dict]) -> list[dict]:
    """
    Return the current report items blocked by credit for dedicated follow-up.
    """
    blocked_items = [item for item in action_items if "credit_block" in item["signals"]]
    blocked_items.sort(
        key=lambda item: (
            item["customer_name"],
            item["pedido"],
            item["seq"],
        )
    )
    return blocked_items[:20]


def _build_status_board(action_items: list[dict]) -> list[dict]:
    """
    Summarize order status pressure by client for compact visual cards.
    """
    counts_by_client = defaultdict(lambda: {"production": 0, "stock": 0, "delay": 0})

    for item in action_items:
        client_counts = counts_by_client[item["customer_name"]]
        if "production_follow_up" in item["signals"]:
            client_counts["production"] += 1
        if "stock_balance" in item["signals"]:
            client_counts["stock"] += 1
        if "delivery_attention" in item["signals"]:
            client_counts["delay"] += 1

    rows = []
    for customer_name, counts in counts_by_client.items():
        total = counts["production"] + counts["stock"] + counts["delay"]
        if total == 0:
            continue
        rows.append(
            {
                "customer_name": customer_name,
                "production": counts["production"],
                "stock": counts["stock"],
                "delay": counts["delay"],
                "total": total,
            }
        )

    rows.sort(key=lambda row: (row["total"], row["delay"], row["stock"], row["customer_name"]), reverse=True)
    max_total = max((row["total"] for row in rows), default=1)
    for row in rows:
        row["production_pct"] = int((row["production"] / max_total) * 100) if max_total else 0
        row["stock_pct"] = int((row["stock"] / max_total) * 100) if max_total else 0
        row["delay_pct"] = int((row["delay"] / max_total) * 100) if max_total else 0
    return rows[:6]


def _build_stock_snapshot(summary: dict) -> dict:
    """
    Build the compact stock split card inspired by executive dashboards.
    """
    in_production = parse_decimal(summary["total_in_production"])
    pending = parse_decimal(summary["total_open_balance"])
    base = in_production + pending
    if base <= 0:
        return {
            "total": summary["total_open_balance"],
            "in_production": summary["total_in_production"],
            "pending": summary["total_open_balance"],
            "in_production_pct": 0,
            "pending_pct": 0,
        }

    return {
        "total": summary["total_open_balance"],
        "in_production": summary["total_in_production"],
        "pending": summary["total_open_balance"],
        "in_production_pct": int((in_production / base) * 100),
        "pending_pct": max(0, 100 - int((in_production / base) * 100)),
    }


def _build_production_board(action_items: list[dict]) -> list[dict]:
    """
    Highlight clients that need production follow-up.
    """
    by_client = defaultdict(lambda: {"count": 0, "late": 0})
    for item in action_items:
        if "production_follow_up" not in item["signals"]:
            continue
        client_stats = by_client[item["customer_name"]]
        client_stats["count"] += 1
        if "delivery_attention" in item["signals"]:
            client_stats["late"] += 1

    rows = []
    max_count = max((stats["count"] for stats in by_client.values()), default=1)
    for customer_name, stats in by_client.items():
        late_ratio = int((stats["late"] / stats["count"]) * 100) if stats["count"] else 0
        rows.append(
            {
                "customer_name": customer_name,
                "count": stats["count"],
                "late_ratio": late_ratio,
                "bar_pct": int((stats["count"] / max_count) * 100) if max_count else 0,
            }
        )

    rows.sort(key=lambda row: (row["count"], row["late_ratio"], row["customer_name"]), reverse=True)
    return rows[:6]


def _build_compact_flag_list(action_items: list[dict], signal_key: str, limit: int = 4) -> list[dict]:
    """
    Build small list cards for one signal.
    """
    rows = [item for item in action_items if signal_key in item["signals"]]
    rows.sort(
        key=lambda item: (
            item["priority_score"],
            item["customer_open_value"],
            item["customer_name"],
            item["pedido"],
        ),
        reverse=True,
    )
    return rows[:limit]


def _build_high_value_clients(client_rows: list[dict], high_value_customer_ids: set) -> list[dict]:
    rows = [
        row for row in client_rows
        if row["customer_id"] in high_value_customer_ids
    ]
    rows.sort(key=lambda row: row["open_value_decimal"], reverse=True)
    return rows[:4]


def _build_clients_with_flags(action_items: list[dict]) -> list[dict]:
    """
    Summarize the most flag-heavy clients for a compact card.
    """
    labels_by_client = defaultdict(list)
    counts_by_client = defaultdict(int)

    for item in action_items:
        counts_by_client[item["customer_name"]] += 1
        for signal in item["signals"]:
            label = BUCKET_LABELS[signal]
            if label not in labels_by_client[item["customer_name"]]:
                labels_by_client[item["customer_name"]].append(label)

    rows = []
    for customer_name, count in counts_by_client.items():
        labels = labels_by_client[customer_name][:2]
        rows.append(
            {
                "customer_name": customer_name,
                "count": count,
                "summary": " + ".join(labels),
            }
        )

    rows.sort(key=lambda row: (row["count"], row["customer_name"]), reverse=True)
    return rows[:4]


def _build_support_exception_rows(
    credit_blocked_orders: list[dict],
    exception_panel: list[dict],
) -> list[dict]:
    rows = []
    seen = set()

    for item in credit_blocked_orders:
        row_key = ("credit_block", item["customer_name"], item["pedido"], item["seq"])
        if row_key in seen:
            continue
        seen.add(row_key)
        rows.append(
            {
                "signal_label": "Bloqueio de Credito",
                "customer_name": item["customer_name"],
                "pedido": item["pedido"],
                "seq": item["seq"],
                "dt_entr": item["dt_entr"],
                "reason_text": item.get("reason_text", ""),
                "next_action": item.get("next_action", ""),
            }
        )

    for section in exception_panel:
        for item in section["items"]:
            row_key = (section["key"], item["customer_name"], item["pedido"], item["seq"])
            if row_key in seen:
                continue
            seen.add(row_key)
            rows.append(
                {
                    "signal_label": section["label"],
                    "customer_name": item["customer_name"],
                    "pedido": item["pedido"],
                    "seq": item["seq"],
                    "dt_entr": item["dt_entr"],
                    "reason_text": item.get("reason_text", ""),
                    "next_action": item.get("next_action", ""),
                }
            )

    return rows[:12]


def _build_support_client_rows(
    client_rows: list[dict],
    high_value_rows: list[dict],
    flagged_rows: list[dict],
) -> list[dict]:
    high_value_names = {row["customer_name"] for row in high_value_rows}
    flagged_names = {row["customer_name"] for row in flagged_rows}
    selected_names = high_value_names | flagged_names

    rows = []
    for row in client_rows:
        if row["customer_name"] not in selected_names:
            continue

        if row["customer_name"] in high_value_names and row["customer_name"] in flagged_names:
            support_label = "Cliente de Alto Valor + Flags"
        elif row["customer_name"] in high_value_names:
            support_label = "Cliente de Alto Valor"
        else:
            support_label = "Clientes com Flags"

        rows.append(
            {
                "customer_name": row["customer_name"],
                "support_label": support_label,
                "total_valor": row["total_valor"],
                "action_flag_count": row["action_flag_count"],
                "focus_reason": row["focus_reason"],
                "next_reading": row["next_reading"],
                "open_value_decimal": row["open_value_decimal"],
            }
        )

    rows.sort(
        key=lambda row: (
            row["open_value_decimal"],
            row["action_flag_count"],
            row["customer_name"],
        ),
        reverse=True,
    )
    return rows[:8]


def _build_operational_comparison(total_lines: int, overdue_lines: int) -> dict:
    """
    Compare overdue order lines against the full report line count.
    """
    late_pct = int((overdue_lines / total_lines) * 100) if total_lines else 0
    return {
        "late_lines": overdue_lines,
        "total_lines": total_lines,
        "late_pct": late_pct,
    }


def _build_ranked_quantity_chart(aggregates: dict[str, Decimal], *, top_n: int = 5) -> list[dict]:
    """
    Convert quantity aggregates into chart rows with normalized bar widths.
    """
    filtered_rows = [
        (customer_name, value)
        for customer_name, value in aggregates.items()
        if value > 0
    ]
    filtered_rows.sort(key=lambda entry: (entry[1], entry[0]), reverse=True)
    top_rows = filtered_rows[:top_n]
    remainder_total = sum((value for _, value in filtered_rows[top_n:]), Decimal("0"))
    if remainder_total > 0:
        top_rows.append(("Outros", remainder_total))
    max_value = max((value for _, value in top_rows), default=Decimal("0"))

    chart_rows = []
    for customer_name, value in top_rows:
        chart_rows.append(
            {
                "customer_name": customer_name,
                "value": format_quantity(value),
                "bar_pct": int((value / max_value) * 100) if max_value > 0 else 0,
            }
        )
    return chart_rows


def _build_dual_value_chart(
    stock_values: dict[str, Decimal],
    delay_values: dict[str, Decimal],
    *,
    top_n: int = 5,
) -> list[dict]:
    """
    Build grouped chart rows for overdue produced value and overdue demand value.
    """
    combined = []
    for customer_name in set(stock_values) | set(delay_values):
        stock_value = stock_values.get(customer_name, Decimal("0"))
        delay_value = delay_values.get(customer_name, Decimal("0"))
        total_value = stock_value + delay_value
        if total_value <= 0:
            continue
        combined.append((customer_name, stock_value, delay_value, total_value))

    combined.sort(key=lambda entry: (entry[3], entry[0]), reverse=True)
    top_rows = combined[:top_n]
    remaining_stock_value = sum((stock_value for _, stock_value, _, _ in combined[top_n:]), Decimal("0"))
    remaining_delay_value = sum((delay_value for _, _, delay_value, _ in combined[top_n:]), Decimal("0"))
    remaining_total = remaining_stock_value + remaining_delay_value
    if remaining_total > 0:
        top_rows.append(("Outros", remaining_stock_value, remaining_delay_value, remaining_total))
    max_value = max((max(stock_value, delay_value) for _, stock_value, delay_value, _ in top_rows), default=Decimal("0"))

    chart_rows = []
    for customer_name, stock_value, delay_value, _ in top_rows:
        chart_rows.append(
            {
                "customer_name": customer_name,
                "stock_value": format_currency(stock_value),
                "delay_value": format_currency(delay_value),
                "stock_bar_pct": int((stock_value / max_value) * 100) if max_value > 0 else 0,
                "delay_bar_pct": int((delay_value / max_value) * 100) if max_value > 0 else 0,
            }
        )
    return chart_rows

def _calculate_overdue_stock_balance(item: dict) -> Decimal:
    """
    Calculate overdue stock balance using the report's explicit open balance.
    """
    return parse_decimal(item.get("sdo_estoq", "0"))


def _calculate_remaining_to_produce(item: dict) -> Decimal:
    """
    Calculate the remaining quantity to produce from ordered, invoiced and open stock.
    """
    return (
        parse_decimal(item.get("qt_ped"))
        - parse_decimal(item.get("qt_fatur"))
        - parse_decimal(item.get("sdo_estoq"))
    )


def build_dashboard(parsed_report, *, today: date | None = None) -> dict:
    """
    Build the full dashboard payload for the latest persisted report.

    The dashboard prefers a fresh parser snapshot of the uploaded TXT file when
    legacy persisted rows are clearly incomplete for display. Otherwise, it uses
    the persisted models directly.
    """
    today = today or date.today()
    near_window = today + timedelta(days=3)
    generated_report_date = parse_report_date(getattr(parsed_report, "generated_date", None))

    customers_payload, report_total = _normalize_from_persistence(parsed_report)
    source = "persisted"

    parser_snapshot = _build_parser_snapshot(parsed_report)
    if parser_snapshot and _should_use_parser_snapshot(customers_payload, report_total):
        customers_payload, report_total = _normalize_from_parser(parsed_report, parser_snapshot)
        source = "parser_snapshot"

    if not any((report_total.get(field) or "").strip() for field in ("total_ped", "total_in_prod", "total_fatur", "total_sdo")):
        report_total = {**report_total, **_compute_summary_from_items(customers_payload)}

    client_open_value_map = {
        customer["customer_id"]: parse_decimal(customer.get("total_valor"))
        for customer in customers_payload
    }
    client_open_qty_map = {
        customer["customer_id"]: parse_decimal(customer.get("total_sdo"))
        for customer in customers_payload
    }

    ranked_customers = sorted(
        customers_payload,
        key=lambda customer: (
            client_open_value_map.get(customer["customer_id"], Decimal("0")),
            client_open_qty_map.get(customer["customer_id"], Decimal("0")),
        ),
        reverse=True,
    )
    high_value_customer_ids = {
        customer["customer_id"]
        for customer in ranked_customers[:3]
        if client_open_value_map.get(customer["customer_id"], Decimal("0")) > 0
        and client_open_qty_map.get(customer["customer_id"], Decimal("0")) > 0
    }

    action_items = []
    customer_action_counts = {
        customer["customer_id"]: 0 for customer in customers_payload
    }
    customer_priority_scores = {
        customer["customer_id"]: 0 for customer in customers_payload
    }
    overdue_orders = set()
    total_order_lines = set()
    falta_produzir_total = Decimal("0")
    em_atraso_total = Decimal("0")
    produzido_data_vencida_total = Decimal("0")
    entrega_esse_mes_total = Decimal("0")
    overdue_weight_by_client = defaultdict(Decimal)
    overdue_stock_by_client = defaultdict(Decimal)
    overdue_stock_value_by_client = defaultdict(Decimal)
    overdue_delay_value_by_client = defaultdict(Decimal)

    for customer in customers_payload:
        for item in customer["items"]:
            open_balance = parse_decimal(item.get("sdo_estoq"))
            produced_qty = parse_decimal(item.get("qt_prod"))
            invoiced_qty = parse_decimal(item.get("qt_fatur"))
            ordered_qty = parse_decimal(item.get("qt_ped"))
            unit_price = parse_decimal(item.get("pre_liq"))
            delivery_date = parse_report_date(item.get("dt_entr"))
            credit_blocked = _is_credit_blocked(item.get("cr_pro")) or _is_credit_blocked(item.get("cr_fat"))
            resolved_ord_prod = _resolve_order_references(item)
            resolved_sit_ordem = _resolve_order_status(item)
            resolved_sit = _resolve_item_status(item)
            has_commercial_identity = bool((item.get("pedido") or "").strip() and (item.get("description") or "").strip())
            signals = []
            remaining_to_produce = _calculate_remaining_to_produce(item)

            if item.get("pedido") and item.get("seq"):
                total_order_lines.add((item.get("pedido"), item.get("seq")))

            falta_produzir_total += remaining_to_produce

            if delivery_date and delivery_date <= today and item.get("pedido") and item.get("seq"):
                overdue_orders.add((item.get("pedido"), item.get("seq")))
                em_atraso_total += remaining_to_produce
                produzido_data_vencida_total += _calculate_overdue_stock_balance(item)
                clamped_remaining = max(Decimal("0"), remaining_to_produce)
                overdue_weight_by_client[customer["customer_name"]] += clamped_remaining
                overdue_stock_by_client[customer["customer_name"]] += open_balance
                overdue_stock_value_by_client[customer["customer_name"]] += open_balance * unit_price
                overdue_delay_value_by_client[customer["customer_name"]] += clamped_remaining * unit_price

            if (
                generated_report_date
                and delivery_date
                and delivery_date.month == generated_report_date.month
                and delivery_date.year == generated_report_date.year
                and ordered_qty > 0
            ):
                entrega_esse_mes_total += ordered_qty

            if open_balance > 0:
                signals.append("stock_balance")

            if credit_blocked and has_commercial_identity:
                signals.append("credit_block")

            if open_balance > 0 and (
                produced_qty > 0
                or _is_production_signal(resolved_sit)
                or _is_production_signal(resolved_sit_ordem)
            ) and invoiced_qty < produced_qty:
                signals.append("production_follow_up")

            if not resolved_ord_prod and has_commercial_identity:
                signals.append("missing_production_reference")

            if open_balance > 0:
                if delivery_date and delivery_date <= near_window:
                    signals.append("delivery_attention")
                elif not item.get("dt_entr") and "missing_production_reference" not in signals:
                    signals.append("delivery_attention")

            if customer["customer_id"] in high_value_customer_ids and open_balance > 0:
                signals.append("high_value_customer")

            if not signals:
                continue

            unique_signals = []
            for signal in signals:
                if signal not in unique_signals:
                    unique_signals.append(signal)

            primary_bucket = next(
                bucket for bucket in PRIMARY_BUCKET_ORDER if bucket in unique_signals
            )
            priority_score = sum(BUCKET_WEIGHTS[signal] for signal in unique_signals)

            signal_badges = [
                {"key": signal, "label": BUCKET_LABELS[signal]}
                for signal in unique_signals
            ]

            action_item = {
                "item_id": item["item_id"],
                "customer_id": customer["customer_id"],
                "representative": customer["representative"],
                "customer_name": customer["customer_name"],
                "pedido": item.get("pedido", ""),
                "seq": item.get("seq", ""),
                "description": item.get("description", ""),
                "larg": item.get("larg", ""),
                "ord_prod": resolved_ord_prod,
                "sit_ordem": resolved_sit_ordem,
                "sit": resolved_sit,
                "dt_entr": item.get("dt_entr", ""),
                "qt_ped": item.get("qt_ped", ""),
                "qt_prod": item.get("qt_prod", ""),
                "qt_fatur": item.get("qt_fatur", ""),
                "sdo_estoq": item.get("sdo_estoq", ""),
                "transp": item.get("transp", ""),
                "cr_pro": item.get("cr_pro", ""),
                "cr_fat": item.get("cr_fat", ""),
                "o_compra": item.get("o_compra", ""),
                "item_cli": item.get("item_cli", ""),
                "signals": unique_signals,
                "signal_badges": signal_badges,
                "primary_bucket": primary_bucket,
                "primary_bucket_label": BUCKET_LABELS[primary_bucket],
                "priority_score": priority_score,
                "open_balance_value": open_balance,
                "customer_open_value": client_open_value_map[customer["customer_id"]],
            }
            action_item["reason_text"] = _build_reason_text(unique_signals)
            action_item["next_action"] = _build_next_action(unique_signals)
            action_item["deadline_label"] = _build_deadline_label(unique_signals, delivery_date, today)
            action_item["priority_label"] = _build_priority_label(unique_signals, delivery_date, today)
            action_items.append(action_item)
            customer_action_counts[customer["customer_id"]] += 1
            customer_priority_scores[customer["customer_id"]] = max(
                customer_priority_scores[customer["customer_id"]],
                priority_score,
            )

    action_items.sort(
        key=lambda item: (
            item["priority_score"],
            item["customer_open_value"],
            item["open_balance_value"],
            item["customer_name"],
            item["pedido"],
            item["seq"],
        ),
        reverse=True,
    )

    action_queue = []
    for bucket_key, bucket_label, description in BUCKET_CONFIG:
        bucket_items = [
            item for item in action_items if bucket_key in item["signals"]
        ]
        action_queue.append(
            {
                "key": bucket_key,
                "label": bucket_label,
                "description": description,
                "count": len(bucket_items),
                "customer_count": len({item["customer_id"] for item in bucket_items}),
                "items": bucket_items,
            }
        )

    client_rows = []
    for customer in customers_payload:
        client_rows.append(
            {
                "customer_id": customer["customer_id"],
                "representative": customer["representative"],
                "customer_name": customer["customer_name"],
                "total_ped": customer.get("total_ped", ""),
                "total_in_prod": customer.get("total_in_prod", ""),
                "total_fatur": customer.get("total_fatur", ""),
                "total_sdo": customer.get("total_sdo", ""),
                "total_valor": customer.get("total_valor", ""),
                "action_flag_count": customer_action_counts[customer["customer_id"]],
                "action_priority": customer_priority_scores[customer["customer_id"]],
                "open_value_decimal": client_open_value_map[customer["customer_id"]],
            }
        )

    client_rows = _enrich_client_rows(client_rows, action_items)

    exception_keys = {"delivery_attention", "missing_production_reference"}
    exception_panel = [
        {
            "key": bucket["key"],
            "label": bucket["label"],
            "items": bucket["items"][:12],
        }
        for bucket in action_queue
        if bucket["key"] in exception_keys
    ]

    flag_matrix = _compute_client_flag_map(action_items, client_rows, high_value_customer_ids)
    client_360 = _build_client_360(client_rows, action_items, flag_matrix)
    delivery_timeline = _build_delivery_timeline(action_items, generated_report_date, today)
    credit_blocked_orders = _build_credit_blocked_orders(action_items)
    status_board = _build_status_board(action_items)
    stock_snapshot = _build_stock_snapshot(summary={
        "total_in_production": report_total.get("total_in_prod", "") or "0",
        "total_open_balance": report_total.get("total_sdo", "") or "0",
    })
    production_board = _build_production_board(action_items)
    delivery_attention_card = _build_compact_flag_list(action_items, "delivery_attention")
    high_value_card = _build_high_value_clients(client_rows, high_value_customer_ids)
    clients_with_flags = _build_clients_with_flags(action_items)
    support_exception_rows = _build_support_exception_rows(
        credit_blocked_orders,
        exception_panel,
    )
    support_client_rows = _build_support_client_rows(
        client_rows,
        high_value_card,
        clients_with_flags,
    )
    operational_comparison = _build_operational_comparison(
        total_lines=len(total_order_lines),
        overdue_lines=len(overdue_orders),
    )
    overdue_weight_chart = _build_ranked_quantity_chart(overdue_weight_by_client)
    overdue_stock_chart = _build_ranked_quantity_chart(overdue_stock_by_client)
    overdue_value_chart = _build_dual_value_chart(
        overdue_stock_value_by_client,
        overdue_delay_value_by_client,
    )

    average_price = _calculate_average_price_from_items(customers_payload, report_total)
    if average_price is None:
        average_price = _calculate_average_price(
            report_total.get("total_valor", "") or "0",
            report_total.get("total_ped", "") or "0",
        )

    summary = {
        "total_clients": len(client_rows),
        "total_ordered": report_total.get("total_ped", "") or "0",
        "total_in_production": report_total.get("total_in_prod", "") or "0",
        "total_invoiced": report_total.get("total_fatur", "") or "0",
        "total_open_balance": report_total.get("total_sdo", "") or "0",
        "total_report_value": report_total.get("total_valor", "") or "-",
        "average_price": average_price,
        "falta_produzir": format_quantity(falta_produzir_total),
        "em_atraso": format_quantity(em_atraso_total),
        "entrega_esse_mes": format_quantity(entrega_esse_mes_total),
        "produzido_data_vencida": format_quantity(produzido_data_vencida_total),
        "pedidos_em_atraso": len(overdue_orders),
        "actionable_item_count": len(action_items),
        "actionable_client_count": sum(
            1 for row in client_rows if row["action_flag_count"] > 0
        ),
        "overdue_order_count": len(overdue_orders),
        "overdue_weight": format_quantity(em_atraso_total),
        "overdue_stock_balance": format_quantity(produzido_data_vencida_total),
        "monthly_invoice_weight": format_quantity(entrega_esse_mes_total),
    }

    return {
        "report_meta": _build_report_meta(parsed_report, source),
        "summary": summary,
        "exception_panel": exception_panel,
        "action_counts": {bucket["key"]: bucket["count"] for bucket in action_queue},
        "client_rows": client_rows,
        "worklist_rows": action_items,
        "status_board": status_board,
        "stock_snapshot": stock_snapshot,
        "production_board": production_board,
        "client_360": client_360,
        "delivery_timeline": delivery_timeline,
        "credit_blocked_orders": credit_blocked_orders,
        "delivery_attention_card": delivery_attention_card,
        "high_value_card": high_value_card,
        "clients_with_flags": clients_with_flags,
        "support_exception_rows": support_exception_rows,
        "support_client_rows": support_client_rows,
        "operational_comparison": operational_comparison,
        "overdue_weight_chart": overdue_weight_chart,
        "overdue_stock_chart": overdue_stock_chart,
        "overdue_value_chart": overdue_value_chart,
    }
