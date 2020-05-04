# -*- coding: utf-8 -*-
# © 2018 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class PaletLabelWzd(models.TransientModel):
    _name = 'palet.label.wzd'

    company_text = fields.Text(string='Company Text')
    partner_id = fields.Many2one('res.partner', 'Partner')
    line_ids = fields.One2many('line.palet.label.wzd', 'wzd_id', 'Label lines')   

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        picking = self.env['stock.picking'].browse(
            self.env.context['active_ids'])
        res['partner_id'] = picking.partner_id.id
        text = "Orballo Innovaciones forestales S.L\n"
        text += "Polígono Industrial de Iñas Rúa Barbanza 2  NAVE 13\n"
        text += "Viveiro de empresas CP 15171 Oleiros\n"
        text += "www.orballo.eu"
        res['partner_id'] = picking.partner_id.id
        res['company_text'] = text
        return res
     
    def print_label(self):
        self.ensure_one()
        model = self.env.context.get('active_model')
        picking = self.env[model].browse(self.env.context.get('active_id'))
        self.ensure_one()
        report_name = 'orb_custom_documents.palet_label'
        data_dic = {
           'model': self._name,
           'wzd_id': self.id
        }
        # Esto devolverá el report pasando por el parser
        return {
            'type': 'ir.actions.report',
            'report_name': report_name,
            'report_type': 'qweb-pdf',
            'data': data_dic,
            }


class LinePaletLabelWzd(models.TransientModel):
    _name = 'line.palet.label.wzd'

    wzd_id = fields.Many2one('palet.label.wzd', 'Wizard')
    sequence = fields.Integer('Sequence')
    lot_id = fields.Many2one('stock.production.lot', 'Lot')
    life_date = fields.Date('Life date')
    name1 = fields.Char('Name 1')
    name2 = fields.Char('Name 2')
    ean13 = fields.Char('Ean 13')
    qty_box = fields.Integer(string='Box grouped', default=240)
    qty_ud = fields.Integer(string='Individual bulk', default=1920)
    barcode = fields.Char('Barcode', compute='_get_barcode')
    barcode_text = fields.Char('Barcode Text', compute='_get_barcode')

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.lot_id:
            lot = self.lot_id
            if lot.label_ean13:
                self.ean13 = lot.label_ean13
            elif lot.product_id.barcode and len(lot.product_id.barcode) == 13:
                self.ean13 = lot.product_id.barcode
            # self.ean13 = '8437017636229'
            self.name1 = lot.product_id.name.upper()
            # self.name2 = 'PEQUEÑO DORMILÓN'
            self.life_date =  lot.life_date

    @api.depends('lot_id', 'ean13')
    def _get_barcode(self):
        for line in self:
            if not line.lot_id or not line.ean13:
                continue
            code_type = '(01)'
            ean14 = line.lot_id.label_palet_ean14
            qty_type = '(30)'
            qty = str(line.qty_box).zfill(4)
            date_type = '(15)'
            date_split = line.life_date.split('-')
            date = date_split[2] + date_split[1] + date_split[0]
            batch_type = '(10)'
            lot_name = line.lot_id.name
            label_text = ''.join([code_type, ean14, qty_type, qty, date_type, date, batch_type, lot_name])
            line.barcode_text = label_text
            line.barcode = line.barcode_text.replace(' ', '').replace('(', '').replace(')', '')
