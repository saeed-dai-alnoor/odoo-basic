{
    'name': 'Sale CEO Approval',
    'version': '1.0',
    'summary': 'Require CEO approval for high-value sale orders',
    'category': 'Sales',
    'depends': ['sale_management'],
    'data': [
        'security/ceo_security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
