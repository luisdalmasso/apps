# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2019 Marlon Falcón Hernandez
#    (<http://www.falconsolutions.cl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Crm Product - MFH',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'maintainer': 'Falcon Solutions',
    'website': 'http://www.falconsolutions.cl',
    'author': 'Falcon Solutions SpA',
    'summary': 'CRM',
    'license': 'AGPL-3',
    'depends': ['sale','crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_product_data.xml',
        'views/crm_lead_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'application': False,
    'auto_install': False
}
