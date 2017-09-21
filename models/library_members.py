# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class LibraryMember(models.Model):

    _inherit = 'res.partner'
    _name = 'library.members'

    isbn = fields.Integer(
        string='code',
    )

    @api.model
    def get_all_librarys(self):
        librarys_model = self.env['library.book']

        #admin

        admin_partners = self.env['res.partner'].browse(3)

        vals= {
            'name' : 'Bilioteca 6',
            'partner_id' : admin_partners.id,
        }

        library_new = librarys_model.create(vals)
        return library_new

        #return librarys_model.search([])

