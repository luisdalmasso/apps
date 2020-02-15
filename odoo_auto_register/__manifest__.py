# -*- coding: utf-8 -*-

{
    'name': 'Odoo Auto Register',
    'version': '13.1',
    'category': 'Website',
    'author': 'Givemerp',
    'depends': ['base', 'website'],
    'data': [
        'data/template_email.xml',
        'views/res_users_view.xml',
        'views/assets_view.xml',
        'views/register_view.xml',
        'data/ir_config_parameter.xml',
    ],
    'installable': True,
    'application': False,
}
