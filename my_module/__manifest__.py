{
    'name': 'My Module',
    'version': '1.0',
    'summary': 'My first Odoo module',
    'author': 'Saeed',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': True,
}
