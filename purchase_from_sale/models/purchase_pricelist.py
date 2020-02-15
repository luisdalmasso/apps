from odoo import api, fields, models

RO_STATES = {'done': [('readonly', True)]}


class PurchasePricelist(models.Model):
    _name = 'purchase.pricelist'
    _description = 'Tarifa de compra'
    _order = 'id desc'
    _inherit = ['mail.thread']

    ref = fields.Char(readonly=True)
    name = fields.Char('Nombre', required=True, track_visibility='onchange', states=RO_STATES)
    date = fields.Datetime('Fecha confirmación', readonly=True, required=True, default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', 'Usuario', default=lambda self: self.env.user, track_visibility='onchange', states=RO_STATES)
    partner_id = fields.Many2one('res.partner', 'Proveedor', required=True, track_visibility='onchange', states=RO_STATES)
    line_ids = fields.One2many('purchase.pricelist.line', 'pricelist_id', 'Productos', states=RO_STATES)
    state = fields.Selection([('draft', 'Cargado'), ('done', 'Confirmado')], 'Estado', required=True, default='draft', track_visibility='onchange')

    def action_confirm(self):
        for record in self:
            for line in record.line_ids:
                variant_seller = line.product_id.variant_seller_ids.filtered(lambda vs: vs.name == record.partner_id)
                if variant_seller:
                    variant_seller.write({'price': line.price, 'pricelist_id': record.id})
                else:
                    variant_seller.create({
                        'name': record.partner_id.id,
                        'price': line.price,
                        'product_id': line.product_id.id,
                        'product_tmpl_id': line.product_id.product_tmpl_id.id,
                        'pricelist_id': record.id,
                        'min_qty': 1,
                    })
            record.state = 'done'

    def name_get(self):
        return [(record.id, '[%s] %s' % (record.ref, record.name)) for record in self]
            

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env['ir.sequence'].next_by_code
        for val in vals_list:
            val['ref'] = sequence('purchase.pricelist')
        return super().create(vals_list)


class PurchasePricelistLine(models.Model):
    _name = 'purchase.pricelist.line'
    _description = 'Línea de tarifa de compra'

    pricelist_id = fields.Many2one('purchase.pricelist', 'Tarifa')
    product_id = fields.Many2one('product.product', 'Producto', required=True, domain=[('purchase_ok', '=', True)])
    price = fields.Float('Precio', required=True)
