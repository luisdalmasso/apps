from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_ids = fields.Many2many('purchase.order', 'sale_purchase_rel', 'sale_id', 'purchase_id', 'Compras')
    total_purchases = fields.Integer('Cantidad de compras', compute='_compute_total_purchases')

    @api.depends('purchase_order_ids')
    def _compute_total_purchases(self):
        for record in self:
            record.total_purchases = len(record.purchase_order_ids)

    def action_view_purchases(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': '%s: Compras' % self.name,
            'res_model': 'purchase.order',
            'view_mode': 'tree,calendar,pivot,graph,form',
            'domain': [('id', 'in', self.purchase_order_ids.ids)]
        }
        if len(self.purchase_order_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.purchase_order_ids.id
            })
        return action
