# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    label_barcode = fields.Char(string='Label Uom', compute='_get_barcode')

    def _get_barcode(self):
       for lot in self:
            res = ''
            if lot.product_id.barcode and len(lot.product_id.barcode) == 13:
                ean13 = lot.product_id.barcode
                code_type = '(01)'
                digit = '1'
                ean13_1 = ean13[:7]
                ean13_2 = ean13[8:]
                batch_type = '(10)'
                control = '1'
                res = ' '.join([code_type, digit, ean13_1, ean13_2, control, batch_type, lot.name])
            lot.label_barcode = res