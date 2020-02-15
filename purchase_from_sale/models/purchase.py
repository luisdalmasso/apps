from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_ids = fields.Many2many('sale.order', 'sale_purchase_rel', 'purchase_id', 'sale_id', 'Ventas')
    sale_order_count = fields.Integer('Cantidad de ventas', compute='_compute_sales_count')

    @api.depends('sale_order_ids')
    def _compute_sales_count(self):
        for record in self:
            record.sale_order_count = len(record.sale_order_ids)

    def action_view_sales(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': '%s: Ventas' % self.name,
            'res_model': 'sale.order',
            'view_mode': 'tree,calendar,pivot,graph,form',
            'domain': [('id', 'in', self.sale_order_ids.ids)]
        }
        if len(self.sale_order_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.sale_order_ids.id
            })
        return action

    def _merge_order_lines(self):
        for order in self:
            products = {}
            for line in order.order_line:
                key = '%d:%.8f' % (line.product_id.id, line.price_unit)
                if key not in products:
                    products[key] = line
                else:
                    products[key].product_qty += line.product_qty
                    line.unlink()
