# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpProductProduceLine(models.TransientModel):
    _inherit = "mrp.product.produce.line"
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if self.product_produce_id:
            lines = self.product_produce_id.produce_line_ids.filtered(lambda p: p.product_id == self.product_id and p.product_uom_id)
            lines -= self
            if lines:
                self.product_uom_id = lines[0].product_uom_id.id