{
    "name": "Hotel Reservation Reports",
    "version": "14.0.1.0.1",
    "author": "Eng. Fares",
    "license": "AGPL-3",
    "depends": ["hotel_reservation", "report_xlsx", 'web'],
    "data": [
        "security/ir.model.access.csv",
        "report/reservation_report_views.xml",
        "report/payment_invoice_management_template.xml",
        "report/reservation_tax_template.xml",
        "report/reservation_promissory_template.xml",
        "report/reservation_monthly_template.xml",
        "report/reservation_invoice_template.xml",
        "report/reservation_payment_template.xml",
        "report/reservation_financial_template.xml",
        "report/hotel_reservation_reports.xml",
        "report/hotel_reservation_promissory_report_views.xml",
        "report/hotel_reservation_financial_report_views.xml",
        "report/hotel_reservation_payment_report_views.xml",
        "report/hotel_reservation_invoice_report_views.xml",
        "report/hotel_reservation_tax_report_views.xml",
        "report/hotel_reservation_tax_report_xlsx_views.xml",
        "report/payment_invoice_management_report_views.xml",
        "report/hotel_reservation_monthly_report_views.xml",
    ],
    "installable": True,
}
