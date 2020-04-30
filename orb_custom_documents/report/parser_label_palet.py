# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ParserPaletLabelReport(models.AbstractModel):
    _name = "report.orb_custom_documents.palet_label"

    @api.model
    def get_report_values(self, docids, data=None):
        model = data['model']
        docs = self.env[model].browse(data['wzd_id'])
        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data,
            'docs': docs,
        }
