# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class BoxLabelWzd(models.TransientModel):
    _name = 'box.label.wzd'

    label_qty = fields.Integer(string='Label Qty', default=8)
    label_uom = fields.Char(string='Label Uom', default='und')
    label_text = fields.Char(
        string='Label Text', 
        default='ORBALLO INNOVACIONES FORESTALES')
    print_type = fields.Selection(
        [('custom_font', 'Font Type'), ('image', 'Image')],
          string='Print type', default='custom_font')

     
    def print_label(self):
        self.ensure_one()
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        self.ensure_one()
        report_name = 'orb_custom_documents.box_label'
        data_dic = {
            'label_qty': self.label_qty,
            'label_uom': self.label_uom,
            'label_text': self.label_text,
            'lot_id': docs.id,
            'print_type': self.print_type
        }
        # Esto devolverá el report pasando por el parser
        return {
            'type': 'ir.actions.report',
            'report_name': report_name,
            'report_type': 'qweb-pdf',
            'data': data_dic,
            }
