from odoo import api, fields, models

class LibraryBookPublication(models.TransientModel):
    _name = 'library.book.publication.wizard'
    _description = 'Modelo Transiente da class Library Book Wirzard'

    name = fields.Char(u'Nome', required=True)
    date = fields.Date(string="Date", required=False, )
    books_ids = fields.Many2many(
        comodel_name="library.book",
        string="Livros",
    )

    @api.multi
    def save_book(self):
        publications = []
        for record in self:
            for book in record.books_ids:
                publications = {
                    'date' : record.date,
                    'name' : record.name,
                }

                self.env['library.book.publication'].create(publications)

        return {'type':'ir.actions.act_window_close'}





