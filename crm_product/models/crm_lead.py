# -*- coding: utf-8 -*-

from odoo import api, fields, models


class LeadProbability(models.Model):
    """Docstring."""

    _name = 'crm.probability'
    _description = 'Probabilidades'
    _order = "name asc"

    name = fields.Integer('Probabilidad')

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "Esta probabilidad ya se encuentra registrada !"),
    ]


class Lead(models.Model):
    """Docstring."""

    _inherit = 'crm.lead'

    product_id = fields.Many2one('product.product', string='Producto')
    probability_id = fields.Many2one('crm.probability', string='Probabilidad')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """."""
        if self.product_id:
            self.name = self.product_id.name
            self.planned_revenue = self.product_id.product_tmpl_id.list_price

    @api.onchange('probability_id')
    def _onchange_probability_id(self):
        """."""
        self.probability = 0
        if self.probability_id:
            self.probability = self.probability_id.name

    def get_product_name(self, product_id):
        """."""
        return self.env['product.product'].browse(product_id).name

    @api.model
    def create(self, vals):
        """."""
        product_id = vals.get('product_id', False)
        if product_id:
            vals['name'] = self.get_product_name(product_id)
        return super(Lead, self).create(vals)


    def write(self, vals):
        """."""
        product_id = vals.get('product_id', False)
        if vals.get('product_id', False):
            vals['name'] = self.get_product_name(product_id)
        return super(Lead, self).write(vals)
