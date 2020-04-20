# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
import math

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    label_barcode = fields.Char(string='Label Barcode', compute='_get_barcode')
    label_ean13 = fields.Char(string='Label EAN13', compute='_get_barcode')

    @api.model
    def get_control_digit(self, ean13):
        """
        Obtiene el código de control a partir de los 12 dígitos del ean13
        """
        res = '1'
        idx = 1
        sum_digits = 0
        for digit in ean13:
            num = int(digit)
            if idx % 2 == 0:  # par position
                num = num * 3
            sum_digits += num
            idx += 1

        nearest_10_mult = math.ceil(sum_digits / 10.0) * 10
        res = nearest_10_mult - sum_digits
        return str(res)


    def _get_barcode(self):
        """
        El barcode debe ser el EAN14, el ean13 lo calculamos a partir de este y
        el código de barras lo compongo con la info del ean13
        """
        for lot in self:
            res = ''
            ean13 = ''
            ean13_control = ''
            if lot.product_id.barcode and len(lot.product_id.barcode) == 14:
                ean14 = lot.product_id.barcode
                code_type = '(01)'
                digit = '1'
                ean13 = ean14[1:-1]  # EAN13 sin dígito control (12 sígitos)
                ean13_1 = ean13[:7]
                ean13_2 = ean13[7:]
                control = ean14[-1]
                ean13_control = self.get_control_digit(ean13)
                batch_type = '(10)'
                res = ' '.join([code_type, digit, ean13_1, ean13_2, control, batch_type, lot.name])
            lot.label_barcode = res
            lot.label_ean13 = ean13 + ean13_control