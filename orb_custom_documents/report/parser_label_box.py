# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class LocationAccuracyReport(models.AbstractModel):
    _name = "report.orb_custom_documents.box_label"

    @api.model
    def get_report_values(self, docids, data=None):
        model = 'stock.production.lot'
        docs = self.env[model].browse(data['lot_id'])
        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data,
            'docs': docs,
        }
