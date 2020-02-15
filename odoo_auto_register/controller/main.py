# -*- coding: utf-8 -*-

from odoo import http


# class Academy(http.Controller):
#    @http.route('/academy/academy/', auth='public')
#    def index(self, **kw):
#        return "Hello, world"


class MainController(http.Controller):
    """."""

    @http.route('/registrarse', auth='public', website=True)
    def registrarse(self):
        """."""
        contries = http.request.env['res.country'].sudo().search([])
        return http.request.render(
            'odoo_auto_register.website_registrarse',
            {'contries': contries, 'email_exist': False})

    @http.route('/validar', methods=['POST'], auth='public', website=True)
    def validar(self, **post):
        """."""
        obj_user = http.request.env['res.users'].sudo()
        obj_parameter = http.request.env['ir.config_parameter'].sudo()

        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        country_id = int(post.get('country'))

        user_copy = obj_user.search(
            [('duplicate_user', '=', True)], limit=1, order='id desc')

        if not user_copy:
            return http.request.render('website.404')

        user_email = obj_user.search(
            [('login', '=', email), ('email', '=', email)])

        print(1)
        if user_email:
            contries = http.request.env['res.country'].sudo().search([])
            return http.request.render(
                'odoo_auto_register.website_registrarse',
                {'contries': contries, 'email_exist': True,
                 'name': name, 'email': email, 'phone': phone,
                 'contries': contries, 'country': country_id})
        print(2)
        user = user_copy.with_context(
            {'password': '', 'name': name, 'email': email,
             'login': email, 'duplicate_user': False, 'auto_register': True,
             'auto_register_country': country_id, 'auto_phone': phone}).copy()

        print(3)
        parameter = obj_parameter.search([('key', '=', 'odoo.auto.register')])

        if parameter and parameter.value:
            obj_user.email_auto_register(user, parameter.value)

        print(4)
        return http.request.render(
            'odoo_auto_register.website_registro_exitoso', {})
