# -*- coding: utf-8 -*-
import openerp
from openerp import models, fields, api
from openerp.addons.resource.faces import task as Task
from openerp import http
from contextlib import closing

class SesClientPasswordCustomer(models.Model):
    _name = 'ses_client_password.customer'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _mail_post_access = 'read'
    _track = {
        'pass_word': {
            'ses_client_password.mt_pass_word': lambda self, cr, uid, obj, ctx=None: obj.create_uid and obj.create_uid.id > 1,
        },
        'user_name': {
            'ses_client_password.mt_user_name': lambda self, cr, uid, obj, ctx=None: obj.id > 1,
        },
    }
    
    partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    user_name = fields.Char('User name', size=30, required=True, track_visibility='onchange')
    pass_word = fields.Char('Password', size=30, required=True, track_visibility='onchange')
    show_password = fields.Boolean('Show password', default=False)
    active = fields.Boolean('Active', default=True)
    type = fields.Selection([('FTP', 'FTP'), ('Email', 'Email'), ('Odoo', 'Odoo'),('Server','Server')], 'Type',size=30, default='FTP', required=True)
    allowed_users_ids = fields.Many2many('res.users', 'client_pwd_user_rel', 'client_pwd_id', 'uid', 'Allowed users')
    project_id = fields.Many2one('project.project', string='Project')
    url = fields.Char('Url')
    comments = fields.Text('Comments')
    
    def message_track(self, cr, uid, ids, tracked_fields, initial_values, context=None):

        def convert_for_display(value, col_info):
            if not value and col_info['type'] == 'boolean':
                return 'False'
            if not value:
                return ''
            if col_info['type'] == 'many2one':
                return value.name_get()[0][1]
            if col_info['type'] == 'selection':
                return dict(col_info['selection'])[value]
            return value
        
        def format_message(message_description, tracked_values):
            message = ''
            if message_description:
                message = '<span>%s</span>' % message_description
            for name, change in tracked_values.items():
                message += '<div> &nbsp; &nbsp; &bull; <b>%s</b>: ' % change.get('col_info')
                if name != 'pass_word':
                    if change.get('old_value'):
                        message += '%s &rarr; ' % change.get('old_value')                
                    message += '%s</div>' % change.get('new_value')
                if name == 'pass_word':
                    message += 'changed</div>'
            return message
        
        if not tracked_fields:
            return True

        for browse_record in self.browse(cr, uid, ids, context=context):
            initial = initial_values[browse_record.id]
            changes = set()
            tracked_values = {}

            # generate tracked_values data structure: {'col_name': {col_info, new_value, old_value}}
            for col_name, col_info in tracked_fields.items():
                field = self._fields[col_name]
                initial_value = initial[col_name]
                record_value = getattr(browse_record, col_name)

                if record_value == initial_value and getattr(field, 'track_visibility', None) == 'always':
                    tracked_values[col_name] = dict(
                        col_info=col_info['string'],
                        new_value=convert_for_display(record_value, col_info),
                    )
                elif record_value != initial_value and (record_value or initial_value):  # because browse null != False
                    if getattr(field, 'track_visibility', None) in ['always', 'onchange']:
                        tracked_values[col_name] = dict(
                            col_info=col_info['string'],
                            old_value=convert_for_display(initial_value, col_info),
                            new_value=convert_for_display(record_value, col_info),
                        )
                    if col_name in tracked_fields:
                        changes.add(col_name)
            if not changes:
                continue

            # find subtypes and post messages or log if no subtype found
            subtypes = []
            # By passing this key, that allows to let the subtype empty and so don't sent email because partners_to_notify from mail_message._notify will be empty
            if not context.get('mail_track_log_only'):
                for field, track_info in self._track.items():
                    if field not in changes:
                        continue
                    for subtype, method in track_info.items():
                        if method(self, cr, uid, browse_record, context):
                            subtypes.append(subtype)

            posted = False
            for subtype in subtypes:
                subtype_rec = self.pool.get('ir.model.data').xmlid_to_object(cr, uid, subtype, context=context)
                #_logger.debug('subtype %s  found' % subtype)
                if not (subtype_rec and subtype_rec.exists()):
                    #_logger.debug('subtype %s not found' % subtype)
                    continue
                message = format_message(subtype_rec.description if subtype_rec.description else subtype_rec.name, tracked_values)
                self.message_post(cr, uid, browse_record.id, body=message, subtype=subtype, context=context)
                posted = True
            if not posted:
                message = format_message('', tracked_values)
                self.message_post(cr, uid, browse_record.id, body=message, context=context)
        return True

