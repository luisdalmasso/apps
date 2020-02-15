# -*- coding: utf-8 -*-

import csv
import tempfile
import base64
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class UpdateMasiveCsv(models.Model):
    """."""

    _name = 'update.masive.csv'
    _description = 'Update masive csv'
    _order = 'id desc'

    name = fields.Many2one('ir.model', string='Modelo', required=True)
    model_name = fields.Char(
        related='name.model', string="Nombre", readonly=True)
    field_from = fields.Many2one(
        'ir.model.fields', string='Desde Campo', required=True)
    field_from_name = fields.Char(
        related='field_from.name', string="Name", readonly=True)
    field_to = fields.Many2one(
        'ir.model.fields', string='Hasta Campo', required=True)
    field_to_name = fields.Char(
        related='field_to.name', string="Nombre", readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('applied', 'Applied')],
        string='Estado', required=True, default='draft')
    file_name = fields.Char('File Name')
    csv = fields.Binary(string='Archivo csv', attachment=True, required=True)

    @api.onchange('name')
    def onchange_name_model(self):
        """."""
        self.field_from = False
        self.field_to = False

    def unlink(self):
        """."""
        if self.state != 'draft':
            raise UserError(_(
                'No puedes eliminar registros en estado diferente a borrador!'))
        return super(UpdateMasiveCsv, self).unlink()

    def action_update(self):
        """."""
        file_name = self.file_name.split('.')
        if file_name[-1].lower() != 'csv':
            raise UserError(_(
                'Invalid file format, file with .csv extension is required!'))

        file_path = '{}/update_masive.csv'.format(tempfile.gettempdir())
        data = self.csv
        f = open(file_path, 'wb')
        f.write(base64.b64decode(data))
        f.close()

        if self.field_from.ttype != self.field_to.ttype:
            raise UserError(_(
                'The types of fields do not match {} not {}'.format(
                    self.field_from.ttype, self.field_to.ttype)))

        lines_csv = csv.reader(open(file_path), delimiter=',')
        check = False
        list_data = []
        head = []
        for line in lines_csv:
            if not check:
                if self.field_from_name != line[0]:
                    raise UserError(_(
                        'The first field of the file does not match: {}'.format(
                            self.field_from_name)))
                if self.field_to_name != line[1]:
                    raise UserError(_(
                        'The second field of the file does not match: {}'.format(
                            self.field_to_name)))
                check = True
                head = line
                continue

            list_data.append((line[0], line[1]))

        obj_model = self.env[self.name.model]

        for i in list_data:
            data_lines = obj_model.search(
                [(head[0], '=', i[0]), (head[1], '!=', False)])
            for x in data_lines:
                x.write({head[1]: i[1]})

        self.browse(self.id).write({'state': 'applied'})
