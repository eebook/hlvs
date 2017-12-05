#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

__author__ = "knarfeh@outlook.com"

import smtplib
import logging
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from celery import Task

from flask import current_app
from jinja2 import Template
from .. import get_template_content
from api.celery import celery_app
from config import config
from api.common.utils import str2bool


LOGGER = logging.getLogger(__name__)
Config = config['dev']


@celery_app.task(serializer='msgpack', max_retries=3)
def send_email(_data):
    """
    class method to send an email
    """
    email_type = _data.get('email_type')
    recipient_list = _data.get('recipient_list')
    language_code = _data.get('language_code', Config.USER_DEFAULT_LANGUAGE)
    params = _data.get('params')
    email_format = _data.get('email_format', 'txt')

    LOGGER.info('[send email]Type: %s, recipient_list: %s', email_type, recipient_list)
    # TODO: recipient should be list
    LOGGER.debug('current_app config: %s', Config.EMAIL_CONFIG)

    template_path = '/'.join(['api/template', Config.EMAIL_CONFIG['template_path'], language_code, email_type])
    subject_template_path = '.'.join([template_path, 'subject'])
    message_template_path = '.'.join([template_path, 'message', email_format])

    sender = Config.EMAIL_CONFIG['sender']
    email_param = params or dict()
    email_param.update({'eebook_url': Config.EMAIL_CONFIG['eebook_url']})

    # Build messager
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ','.join(recipient_list)
    subject_template = get_template_content(subject_template_path)
    message_template = get_template_content(message_template_path)
    msg['Subject'] = Header(Template(subject_template).render(email_param))
    if email_format == 'html':
        msg.attach(MIMEText(Template(message_template).render(email_param), 'html', 'utf8'))
    else:
        msg.attach(MIMEText(Template(message_template).render(email_param), 'plain', 'utf8'))

    if Config.DEBUG is True:
        debug_cc_email = Config.EMAIL_CONFIG['debug_cc_email'] or None
        if debug_cc_email:
            msg['Bcc'] = debug_cc_email
            if debug_cc_email not in recipient_list:  # TODO: do we need it
                recipient_list.append(debug_cc_email)
    if str2bool(Config.EMAIL_USE_HTTP):
        requests.post(
            "https://api.mailgun.net/v3/"+Config.MAILGUN_CONFIG['MAIL_DOMAIN_NAME']+'/messages',
            auth=("api", Config.MAILGUN_CONFIG["MAIL_API_KEY"]),
            data={
                "from": sender,
                "to": recipient_list,
                "suject": Template(subject_template).render(email_param),
                "text": Template(message_template).render(email_param)
            }
        )
        return

    server = None
    exception_traceback = None
    SMTP = Config.SMTP
    try:
        LOGGER.debug("Using SMTP with ssl")
        server = smtplib.SMTP_SSL(host=SMTP['server'], port=SMTP['port'])
        if SMTP['username'] != '' and SMTP['password'] != '':
            server.login(SMTP['username'], SMTP['password'])
        server.sendmail(sender, recipient_list, msg.as_string())
    except Exception as e:
        LOGGER.error("Failed to send email, error: %s", e)
        exception_traceback = traceback.format_exc()
    finally:
        if server:
            server.quit()
            LOGGER.info('[send email] server quit')

    # TODO: add email trace

