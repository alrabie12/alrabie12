{
    "name": "Hr Resignation",
    "version": "14.0.1.0.1",
    "author": "Hadooc",
    "depends": [
        "request",
        "request_refuse",
        "hr_employee_number",
        "hr_contract",
        "hr_base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/hr_resignation_security.xml",
        "data/mail_data.xml",
        "data/hr_resignation_data.xml",
        "report/clearance_certificate_report.xml",
        "views/hr_resignation_views.xml",
        "views/request_type_views.xml",
        "views/request_stage_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
}
