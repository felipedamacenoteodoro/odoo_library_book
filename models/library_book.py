# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from datetime import timedelta
from odoo import models, fields,api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class LibraryBook(models.Model):

    _name = b'library.book'
    _inherit = ['mail.thread']
    # _description = 'Library Book'
    # _order = 'date_release desc, name'
    # _rec_name = 'short_name'

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be unique.')
    ]



    name = fields.Char(u'Nome', required=True)
    short_name = fields.Char('Short Title')
    date = fields.Date('Data')
    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Parceiro',
    )

    diretor = fields.Many2one(
        comodel_name='res.users',
        string='Diretor Autoritario',
        required=True,
    )

    contato = fields.Char(string="Contato", required=False, )

    descricao = fields.Char(
        string='Descricao',
        compute='_compute_descricao'
    )

    currency_id = fields.Many2one('res.currency', string='Currency')

    cost_price = fields.Float(
        'Book Cost', dp.get_precision('Book Price'))

    notes = fields.Text('Internal Notes')

    ## Metododos e api decoretor
    state = fields.Selection(
        selection=[
            ('draft', 'Not Avaliable'),
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost')
        ],
        string='State',
        default='draft',
        store=True,
    )

    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer('Number of Pages')
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4),
    )

    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='library_book_attachment_rel',
        column1='library_book_id',
        collumn2='attachment_id',
        string=u'Attachments',
    )

    publisher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )

    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()

    author_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Authors',
    )

    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        search='_search_age',
        store=False,
        compute_sudo=False,
    )

    publisher_city = fields.Char(
        string='Publisher City',
        related='publisher_id.city',
        store=True,
    )

    date_release_fmt = fields.Char(
        string=u'Data de lançamento formatada',
        compute='_compute_date_release_fmt',
    )

    @api.depends('date_release')
    def _compute_date_release_fmt(self):
        if self.date_release:
            date_str = self.date_release
            date_fmt = '%s/%s/%s' % (date_str[8:], date_str[5:7], date_str[:4])
            self.date_release_fmt = date_fmt

    @api.depends('diretor','name','date')
    def _compute_descricao(self):
        for record in self:
            descricao = ''
            if record.name:
                descricao = record.name + '  Foi escrito por ' + (record.diretor.name or '')

            if record.date:
                descricao += ' em ' + record.date[:4]
            record.descricao = descricao

    @api.onchange('diretor')
    def _onchange_contato(self):
        for record in self:
            if record.diretor.phone:
               record.contato = record.diretor.phone
            elif record.diretor.email:
                record.contato = record.diretor.email

    #Logica que altera status do livro

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed= [
            ('draft', 'available'),
            ('draft', 'borrowed'),
            ('available', 'borrowed'),
            ('borrowed', 'available'),
            ('available', 'lost'),
            ('borrowed', 'lost'),
            ('lost', 'available'),
        ]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
               raise UserError('This state is no allowed')

    #mudando status

    def action_available(self):
        for record in self:
            record.change_state('available')

    def action_no_allowed(self):
        for record in self:
            if(not record.change_state('no allowed')):
                raise ValidationError('This state is no allowed')

    # @api.constrains('state')
    # def change_on_state(self):
    #     for record in self:
    #         record.change_state('available')

    #Logica que implementa escrita no campo
    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.from_string(fields.Date.today())
        for book in self.filtered('date_release'):
            delta = fields.Date.from_string(book.date_release) - today
            book.age_days = delta.days

    #logica que implementa a pesquisa no campo
    def _search_age(self, operator, value):
        today = fields.Date.from_string(fields.Date.today())
        value_days = timedelta(days=value)
        value_date = fields.Date.to_string(today - value_days)
        return [('date_release', operator, value_date)]

    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise ValidationError('Release date must be in the past')



    def name_get(self):
        result = []
        for record in self:
            result.append((
                record.id, u"%s (%s)" % (record.name, record.date_release)))
        return result





