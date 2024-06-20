{
    'name': 'Product Info Country Wise',
    'version': '1.2',
    'summary': 'Module to demonstrate product description country wise',
    'category': 'Accounting',
    'author': 'Yash Ghadigaonkar',
    'sequence': -10,
    'description': """Module to demonstrate product description country wise""",
    'website': 'www.example.com',
    'license': 'LGPL-3',
    'depends': ['base', 'sale',],
    'data': [
        'views/product_catge_inherit.xml',
        'reports/sales_report_inherit.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
