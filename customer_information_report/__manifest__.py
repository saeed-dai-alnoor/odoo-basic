{
    'name': "Customer Information Report",
    'summary': "A custom PDF report for printing customer details from the form view.",
    'description': """
        This module adds a new print action on the customer form view
        to generate a PDF report with detailed customer information.
    """,
    'author': "Saeed Dev",
    'category': 'Sales',
    'version': '17.0.1.0.0',
    'depends': ['base', 'sale'], # إضافة 'sale' للوصول إلى حقل sale_amount_total
    'data': [
        'reports/customer_report_template.xml',
        'reports/customer_report.xml',
    ],
    'installable': True,
    'application': True,
}