{
    'name': 'Custom Partner',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Adds unique mobile constraint and automatic customer code.',
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_views.xml',
      
    ],
    'installable': True,
    'application': True,
}
