import base64

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class LoadPurchasePricelist(models.TransientModel):
    _name = 'load.purchase.pricelist.wizard'
    _description = 'Carga masiva de productos en tarifa de compra'

    pricelist_id = fields.Many2one('purchase.pricelist', 'Tarifa')
    csv_file = fields.Binary('Archivo CSV', required=True)
    filename = fields.Char('Nombre archivo')
    search_mode = fields.Selection([('barcode', 'Código de barras'),
                                    ('default_code', 'Referencia interna')],
                                   'Buscar por', required=True, default='default_code')

    def load_csv(self):
        data = base64.b64decode(self.csv_file).decode('utf-8')
        product_obj = self.env['product.product']
        vals = []
        for line in data.split('\n'):
            line = line.split(',')
            if len(line) != 2:
                continue
            product = product_obj.search([(self.search_mode, '=', line[0])])
            if not product:
                continue
            found = False
            # Verificando que el producto no esté cargado actualmente
            for pl_line in self.pricelist_id.line_ids:
                if product == pl_line.product_id:
                    vals.append((1, pl_line.id, {'price': float(line[1])}))
                    found = True
                    break
            if not found:
                vals.append((0, 0, {'product_id': product.id, 'price': float(line[1])}))
        if not vals:
            raise ValidationError(_('Archivo CSV sin productos válidos que cargar.'))
        self.pricelist_id.write({'line_ids': vals})
        return {'type': 'ir.actions.act_window_close'}
