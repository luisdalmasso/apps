# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Users(models.Model):
    """."""

    _inherit = 'res.users'

    duplicate_user = fields.Boolean('Duplicar')
    auto_register = fields.Boolean()
    auto_register_country = fields.Many2one('res.country', 'Pais')
    auto_phone = fields.Char('Telefono', size=16)

    def email_auto_register(self, user, email):
        """."""
        ctx = {'email_to': email, 'email_from': email}
        template_id = self.env.ref(
            'odoo_auto_register.template_odoo_auto_register')
        template_id.with_context(ctx).send_mail(user.id, force_send=True)

    def search_email(self, email):
        """."""
        return bool(self.search([('email', '=', email)]))

    def copy(self, default=None):
        """."""
        default = dict(default or {})
        context = self._context
        if context.get('auto_register', False):
            default.update(context)
        return super(Users, self).copy(default)

    @api.model
    def create(self, vals):
        """."""
        if vals.get('auto_register', False):
            if 'allowed_company_ids' in vals:
                del vals['allowed_company_ids']
        return super().create(vals)
