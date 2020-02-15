##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Marlon Falcón Hernandez
#    (<http://www.ynext.cl>).
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
    'name': 'Compra desde Venta MFH',
    'version': '13.0.1.0.0',
    'author': 'Ynext SpA',
    'maintainer': 'Ynext SpA',
    'website': 'http://www.ynext.cl',
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': 'Genera órdenes de compra a partir de una orden de venta.',
    'depends': ['base', 'product', 'purchase', 'sale', 'sales_team'],
    'data': [
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'wizard/purchase_from_sale.xml',
        'wizard/load_purchase_pricelist.xml',
        'views/product.xml',
        'views/purchase_pricelist.xml',
        'views/purchase.xml',
        'views/sale.xml',
    ],
    'images': ['static/description/banner.jpg'],
}
