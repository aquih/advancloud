# -*- encoding: utf-8 -*-

{
    'name' : 'AdvanCloud',
    'version' : '1.0',
    'category': 'Inventory/Inventory',
    'description': """Integración con AdvanCloud de Keonn""",
    'author': 'aquíH',
    'website': 'http://aquih.com/',
    'depends' : [ 'stock' ],
    'data' : [
        'views/res_company_views.xml',
        'views/product_template_views.xml',
        'views/stock_warehouse_views.xml',
        'views/stock_location_views.xml',
        'views/stock_views.xml',
        'wizard/send_products.xml',
        'wizard/get_stock.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'license': 'Other OSI approved licence',
}
