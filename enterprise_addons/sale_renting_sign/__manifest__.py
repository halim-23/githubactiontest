# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Rental/Sign Bridge",
    "summary": """
            Bridge Sign functionalities with the Rental application
        """,
    "author": "Odoo S.A.",
    "website": "https://www.odoo.com",
    "category": "Sales/Sales",
    "version": "1.0",
    "depends": ["sign", "sale_renting"],
    "data": [
        "security/ir.model.access.csv",
        "security/rental_sign_security.xml",
        "wizard/rental_sign_views.xml",
        "data/mail_templates.xml",
        "views/res_config_settings_views.xml",
        "views/sale_rental_views.xml",
    ],
    "demo": [
        "data/demo.xml",
    ],
    "auto_install": False,
    "license": "OEEL-1",
}
