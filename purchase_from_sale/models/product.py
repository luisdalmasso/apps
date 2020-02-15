from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    purchase_price = fields.Monetary('Tarifa de compra', compute='_compute_purchase_price')
    provider_id = fields.Many2one('res.partner', 'Proveedor', compute='_compute_purchase_price')

    @api.depends('variant_seller_ids')
    def _compute_purchase_price(self):
        for record in self:
            record.purchase_price = record.variant_seller_ids and record.variant_seller_ids[0].price
            if record.variant_seller_ids:
                if record.variant_seller_ids[0].name:
                    record.provider_id = record.variant_seller_ids[0].name
            else:
                record.provider_id = False



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    purchase_price = fields.Monetary('Tarifa de compra', compute='_compute_purchase_price')
    provider_id = fields.Many2one('res.partner', 'Proveedor', compute='_compute_purchase_price')

    @api.depends('seller_ids')
    def _compute_purchase_price(self):
        for record in self:
            record.purchase_price = record.seller_ids and record.seller_ids[0].price
            if record.seller_ids:
                if record.seller_ids[0]:
                    record.provider_id = record.seller_ids[0].name
            else:
                record.provider_id = False


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    pricelist_id = fields.Many2one('purchase.pricelist', 'Tarifa de compra', readonly=True)
