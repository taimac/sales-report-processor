from reports.models import (
    ParsedReport,
    CustomerSection,
    ParsedItem,
    ContinuationRow,
    CustomerTotal,
    ReportTotal,
)

from reports.services.txt_parser import assemble_report


def persist_report(uploaded_report):
    """
    Orchestrates the full persistence pipeline for a supplier report.

    This function is responsible for:
    1. Calling the TXT parser to transform the raw file into structured data
    2. Creating a ParsedReport (root entity)
    3. Persisting all related entities:
        - CustomerSection
        - ParsedItem
        - ContinuationRow
        - CustomerTotal
        - ReportTotal

    The function acts as the bridge between:
        raw file → structured data → database records

    Args:
        uploaded_report (UploadedReport):
            The original uploaded file instance.

    Returns:
        ParsedReport:
            The root persisted report object.
    """

    # ---------------------------------------------------------
    # STEP 1 — Parse raw TXT into structured data
    # ---------------------------------------------------------
    # The parser reads the file and returns a dictionary containing:
    # - metadata (date, time)
    # - customers (sections with items)
    # - totals (client + grand totals)
    data = assemble_report(uploaded_report.file.path)

    # ---------------------------------------------------------
    # STEP 2 — Create root ParsedReport
    # ---------------------------------------------------------
    # This is the top-level entity that represents the processed report
    parsed_report = ParsedReport.objects.create(
        uploaded_report=uploaded_report,
        generated_date=data["metadata"].get("generated_date", ""),
        generated_time=data["metadata"].get("generated_time", ""),
    )

    # ---------------------------------------------------------
    # STEP 3 — Persist customer sections and their items
    # ---------------------------------------------------------
    # Each customer section groups multiple items
    for customer_data in data.get("customers", []):
        customer = CustomerSection.objects.create(
            parsed_report=parsed_report,
            representative=customer_data.get("representative", ""),
            customer_name=customer_data.get("customer_name", ""),
        )

        # -----------------------------------------------------
        # STEP 3.1 — Persist items for this customer
        # -----------------------------------------------------
        for item_data in customer_data.get("items", []):
            item = ParsedItem.objects.create(
                customer_section=customer,

                est=item_data.get("est", ""),
                pedido=item_data.get("pedido", ""),
                seq=item_data.get("seq", ""),
                descricao=item_data.get("descricao", ""),
                espess=item_data.get("espess", ""),
                larg=item_data.get("larg", ""),
                compr=item_data.get("compr", ""),

                ord_prod=item_data.get("ord_prod", ""),
                sit_ordem=item_data.get("sit_ordem", ""),
                dt_entr=item_data.get("dt_entr", ""),
                aa=item_data.get("aa", ""),

                qt_ped=item_data.get("qt_ped", ""),
                qt_pc=item_data.get("qt_pc", ""),
                qt_prod=item_data.get("qt_prod", ""),
                qt_fatur=item_data.get("qt_fatur", ""),
                sdo_estoq=item_data.get("sdo_estoq", ""),

                sit=item_data.get("sit", ""),

                pre_liq=item_data.get("pre_liq", ""),
                pf=item_data.get("pf", ""),
                vlr_peca=item_data.get("vlr_peca", ""),
                pag=item_data.get("pag", ""),
                transp=item_data.get("transp", ""),

                cr_pro=item_data.get("cr_pro", ""),
                cr_fat=item_data.get("cr_fat", ""),
                o_compra=item_data.get("o_compra", ""),
                item_cli=item_data.get("item_cli", ""),
                mnf=item_data.get("mnf", ""),
            )

            # -------------------------------------------------
            # STEP 3.2 — Persist continuation rows (if any)
            # -------------------------------------------------
            # Continuations represent additional production lines
            # linked to the main item
            for cont_data in item_data.get("continuations", []):
                ContinuationRow.objects.create(
                    parsed_item=item,
                    ord_prod=cont_data.get("ord_prod", ""),
                    sit_ordem=cont_data.get("sit_ordem", ""),
                    qt_prod=cont_data.get("qt_prod", ""),
                    sit=cont_data.get("sit", ""),
                )

        # -----------------------------------------------------
        # STEP 4 — Persist customer totals
        # -----------------------------------------------------
        # Totals are extracted separately and aligned by index
        customer_totals = customer_data.get("totals", {}).get("client_totals", [])
        total_data = customer_totals[0] if customer_totals else None

        if total_data:
            CustomerTotal.objects.create(
                customer_section=customer,
                total_ped=total_data.get("total_ped", ""),
                total_in_prod=total_data.get("total_in_prod", ""),
                total_fatur=total_data.get("total_fatur", ""),
                total_sdo=total_data.get("total_sdo", ""),
                total_valor=total_data.get("total_valor", ""),
            )


    # ---------------------------------------------------------
    # STEP 5 — Persist report (grand) totals
    # ---------------------------------------------------------
    grand_totals = data.get("totals", {}).get("grand_totals", [])

    total_data = grand_totals[0] if grand_totals else {}

    ReportTotal.objects.create(
        parsed_report=parsed_report,
        total_ped=total_data.get("total_ped", ""),
        total_in_prod=total_data.get("total_in_prod", ""),
        total_fatur=total_data.get("total_fatur", ""),
        total_sdo=total_data.get("total_sdo", ""),
        total_valor=total_data.get("total_valor", ""),
    )
    
    # ---------------------------------------------------------
    # FINAL STEP — Return root object
    # ---------------------------------------------------------
    return parsed_report