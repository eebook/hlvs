from __future__ import absolute_import
from __future__ import unicode_literals

__author__ = "knarfeh@outlook.com"

import smtplib
import logging
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from flask import current_app
from config import Config

LOGGER = logging.getLogger(__name__)


class Email(object):

    def __init__(self, data):
        self.data = data

    def send(self):
        """
        class method to send an email
        """
        email_type = self.data.get('email_type')
        recipient_list = self.data.get('recipient_list')
        language_code = self.data.get('language_code', current_app.config['USER_DEFAULT_LANGUAGE'])
        params = self.data.get('params')
        email_format = self.data.get('email_format', 'txt')

        LOGGER.info('[send email]Type: %s, recipient_list: %s', email_type, recipient_list)
        # TODO: recipient should be list
        LOGGER.debug('current_app config: %s', current_app.config['EMAIL_CONFIG'])

        template_path = '/'.join(['/api', current_app.config['EMAIL_CONFIG']['template_path'], language_code, email_type])
        LOGGER.debug('template path??? %s', template_path)
        subject_template = '.'.join([template_path, 'subject'])
        message_template = '.'.join([template_path, 'message', email_format])
        LOGGER.debug('subject template??? %s', subject_template)

        sender = current_app.config['EMAIL_CONFIG']['sender']
        email_param = params or dict()
        email_param.update({'eebook_url': current_app.config['EMAIL_CONFIG']['eebook_url']})
        LOGGER.debug('here???')

        # Build messager
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ','.join(recipient_list)
        LOGGER.debug('here??????')

        if current_app.config['DEBUG'] is True:
            debug_cc_email = current_app.config['EMAIL_CONFIG']['debug_cc_email'] or None
            if debug_cc_email:
                msg['Bcc'] = debug_cc_email
                if debug_cc_email not in recipient_list:  # TODO: do we need it
                    recipient_list.append(debug_cc_email)

        msg['Subject'] = Header('subject')  # TODO: use jinja2

        if email_format == 'html':
            pass  # TODO: use jinja2
        else:
            msg.attach(MIMEText('content', 'plain', 'utf8'))

        LOGGER.debug('fuck??????')
        server = None
        exception_traceback = None
        SMTP = current_app.config['SMTP']
        try:
            LOGGER.debug("Using SMTP with ssl")
            server = smtplib.SMTP_SSL(host=SMTP['server'], port=SMTP['port'])
            if SMTP['username'] != '' and SMTP['password'] != '':
                server.login(SMTP['username'], SMTP['password'])
            server.sendmail(sender, recipient_list, msg.as_string())
        except Exception as e:
            LOGGER.error("Failed to send email. %s - %s", type(e), e.message)
            exception_traceback = traceback.format_exc()
        finally:
            if server:
                server.quit()
                LOGGER.info('[send email] server quit')

        # TODO: add email trace

