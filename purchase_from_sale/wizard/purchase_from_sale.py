from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseFromSaleWizard(models.TransientModel):
    _name = 'purchase.from.sale.wizard'
    _description = 'Generar compras desde ventas'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['sale_order_ids'] = self.env.context.get('active_ids')
        return res

    sale_order_ids = fields.Many2many('sale.order', string='Ventas')
    partner_id = fields.Many2one('res.partner', 'Proveedor')

    def action_create_purchases(self):
        purchases = self.env['purchase.order']
        suppliers = {}
        for line in self.sale_order_ids.order_line:
            if not line.product_id:
                # Algunas sale order pueden venir sin producto, estas no se
                # tomarán en cuenta.
                continue
            price = 0.0
            min_qty = 0
            if self.partner_id:
                partner = self.partner_id
            elif line.product_id.variant_seller_ids:
                partner = line.product_id.variant_seller_ids[0].name
                price = line.product_id.variant_seller_ids[0].price
                min_qty = line.product_id.variant_seller_ids[0].min_qty
            else:
                raise ValidationError(_('El producto %s no tiene proveedor.') % line.product_id.display_name)
            line_vals = [(0, 0, {
                'name': line.name,
                'product_id': line.product_id.id,
                'product_qty': min_qty < line.product_uom_qty and line.product_uom_qty or min_qty,
                'product_uom': line.product_uom.id,
                'price_unit': price,
                'date_planned': fields.Datetime.now(),
                'taxes_id': line.product_id.supplier_taxes_id and [(4, line.product_id.supplier_taxes_id.id)]
            })]
            # Se agrupan las compras por proveedor, y por cada línea, si ya tengo
            # una compra con ese proveedor, solo le agrego una línea, si no hay
            # compra de ese proveedor, la creo y la guardo en el diccionario.
            # En cualquier caso, asociamos la orden a la compra.
            if partner in suppliers:
                suppliers[partner].write({'order_line': line_vals, 'sale_order_ids': [(4, line.order_id.id)]})
            else:
                purchase = purchases.create({
                    'partner_id': partner.id,
                    'order_line': line_vals,
                    'sale_order_ids': [(4, line.order_id.id)]
                })
                suppliers[partner] = purchase
                purchases += purchase
        if not purchases:
            raise ValidationError(_('No hay líneas para generar compras.'))
        # Unimos todas las líneas con el mismo producto y precio en una sola línea.
        purchases._merge_order_lines()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Compras',
            'res_model': 'purchase.order',
            'view_mode': 'tree,kanban,pivot,graph,form',
            'domain': [('id', 'in', purchases.ids)]
        }
