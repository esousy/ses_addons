# -*- coding: utf-8 -*-
{
    'name': 'Reveal Password',
    'version': '1.0.0',
    'author': 'sesousy',
    'category': '',
    'website': '',
    'depends': ['project'],
    'data': [
        'views/reveal_password.xml',
        'data/reveal_password.xml',
        'security/reveal_password.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'qweb': ['static/src/xml/reveal_password.xml'],
    'description': '''
        Module to store customers's passwords
    ''',
}
