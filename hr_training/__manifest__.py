{
    "name": "Training Management",
    "version": "14.0.1.0.1",
    "author": "Hadooc",
    "depends": [
        "hr_base",
        "hr_employee_number",
        "request_refuse",
        "request",
        "hr_obligation",
        "web_digital_sign",
        "base_address_city",
    ],
    "data": [
        "security/hr_training_security.xml",
        "security/ir.model.access.csv",
        "data/hr_training_data.xml",
        "data/mail_data.xml",
        "views/menu.xml",
        "report/training_report_template.xml",
        "views/hr_training_views.xml",
        "views/hr_training_setting_views.xml",
        "views/hr_training_center_views.xml",
        "views/hr_views.xml",
        "views/res_users_views.xml",
        "views/request_stage_views.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}