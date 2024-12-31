{
    "name": "Hr Payroll Loan",
    "version": "14.0.1.0.0",
    "author": "Eng. Fares",
    "depends": ["hr_payroll_base", "request", "request_refuse"],
    "data": [
        "security/hr_payroll_loan_security.xml",
        "security/ir.model.access.csv",
        "data/hr_payroll_loan_data.xml",
        "data/mail_data.xml",
        "data/hr_payroll_loan_data.xml",
        "report/hr_payroll_loan_templates.xml",
        "report/hr_payroll_loan_reports.xml",
        "views/menu.xml",
        "wizard/hr_loan_wizard_views.xml",
        "views/hr_loan_views.xml",
        "views/hr_loan_setting_views.xml",
        "views/hr_employee_views.xml",
        "views/request_stage_views.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "license": "AGPL-3",
}
