# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.tools import config


class Partner(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(copy=False)

    _sql_constraints = [
        ('email_partner_uniq', 'unique(email)', 'El correo electrónico del contacto ya existe.'),
    ]

    @api.constrains("vat")
    def _check_vat_unique(self):
        for record in self:
            if record.parent_id or not record.vat:
                continue
            test_condition = config["test_enable"] and not self.env.context.get(
                "test_vat"
            )
            if test_condition:
                continue
            if record.same_vat_partner_id:
                raise ValidationError(
                    ("El RIF o CI %s del contacto ya existe.") % record.vat
                )

    @api.model
    def create(self, vals):
        res = super(Partner, self).create(vals)
        name = vals['name'].upper().strip()
        res.name = name
        if len(self.env['res.partner'].search([('name', '=', name)])) > 1:
            raise ValidationError('El contacto ya está creado.')
        return res
