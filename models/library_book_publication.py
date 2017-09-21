from odoo import api, fields, models

class LibraryBookPublication(models.Model):
    _name = 'library.book.publication'
    _description = 'Modelo da class Library Book Publication'

    name = fields.Char(u'Nome', required=True)
    date = fields.Date(string="Date", required=False, )
    books_ids = fields.Many2many(
        comodel_name="library.book",
        string="Livros",
    )




