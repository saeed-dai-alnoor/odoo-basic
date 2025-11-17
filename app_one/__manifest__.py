{
    'name': 'App One',
    'version': '17.0',
    'author': 'Saeed',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/tree_plant_views.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'app_one/static/src/css/tree_style.css',
    ],
},
    'installable': True,
    'application': True,
}
