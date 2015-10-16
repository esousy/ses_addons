{
    'name': 'Client Password',
    'version': '1.0.0',
    'author': 'sesousy',
    'category': '7Gates',
    'website': '',
    'depends': ['project'],
    'data': [
        'views/ses_client_password.xml',
        'data/ses_client_password.xml',
        'security/ses_client_password.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'qweb': ['static/src/xml/ses_client_password.xml'],
    'description': '''
        Module to store customers's passwords
    ''',
}
