# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'mail.thread']
    name = fields.Char('Name', required=True)  # Modifica o atributo acrescentando o required
    email = fields.Char('Email')
    date = fields.Date('Date')
    is_company = fields.Boolean('Is a company')
    is_editor = fields.Boolean('Is Editor')
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State'
    )

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country'
    )


    parent_id = fields.Many2one(
        comodel_name='res.partner',
        string='Related Company',
    )
    child_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='parent_id',
        string='Contacts',
    )

    book_ids_pub = fields.One2many(
        comodel_name='library.book',
        inverse_name='publisher_id',
        string='Published Book',
    )
    book_ids_aut = fields.Many2many(
        comodel_name='library.book',
        string='Authored Books',
    )

    _order = 'name'

    authored_book_ids = fields.Many2many(
        comodel_name='library.book',
        string='Authored Books',
    )
    count_books = fields.Integer(
        comodel_name='Number of Authored Books',
        compute='_compute_count_books',
    )

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)

    def create_contacts(self):
        today_str = '2017-01-01'

        val1 = {
            'name': u'Eric Idle',
            'email': u'eric.idle@example.com',
            'date': today_str,
        }

        val2 = {
            'name': u'John Cleese',
            'email': u'john.clesse@example.com',
            'date': today_str,
        }

        partner_val = {
            'name': u'Flying Circus',
            'email': u'm.python@example.com',
            'date': today_str,
            'is_company': True,
            'child_ids': [(0, 0, val1),
                          (0, 0, val2),
                          ]
        }

        record = self.env['res.partner'].create(partner_val)


    @api.multi
    def open_commercial_entity(self):
        print('================== Chamou a funcao ============================')
