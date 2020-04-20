# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Orballo Custom Documents',
    'version': '11.0.1.0.0',
    'category': 'Custom Documents',
    'license': 'AGPL-3',
    'author': "Comunitea,",
    'website': 'https://www.comunitea.com',
    'depends': [
        'base',
        'web',
        'sale',
        'stock',
        'product',
        'stock_picking_invoice_link',
    ],
    'data': [
        'views/report_invoice.xml',
        'views/box_label_report.xml',
        'views/product_lot_view.xml',
        'wizard/label_box_wzd.xml',
    ],
    'installable': True,
}
