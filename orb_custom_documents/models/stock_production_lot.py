# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    label_barcode = fields.Char(string='Label Uom', compute='_get_barcode')

    def _get_barcode(self):
       for lot in self:
           res = '(01) 1 8436553 98137 1 (10) 02712'
           lot.label_barcode = res