# -*- coding: utf-8 -*-
{
    'name': "Library Book",
    'summary': "Esta é uma descrição simples do novo módulo que estou desenvolvendo",
    'description': """Este campo deve ser usado para fornecer uma descrição mais completa
                      sobre o módulo o qual estou desenvolvendo""",
    'author': "Felipe D. Teodoro",
    'license': "AGPL-3",
    'website': "http://www.meuwebsite.com.br",
    'category': 'Uncategorized',
    'version': '10.0.1.0.0',
    'depends': [
                'base',
                'mail',
                'decimal_precision',
                'report_py3o'
    ],
    'data': [
        'views/library_book_menu.xml',
        'security/library_book_security.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/library_book_view_kanban.xml',
        'wizard/library_book_publication_wizard.xml',
        'report/report_library_book_py3o.xml',
    ],
    # 'demo': ['demo.xml'],
}

