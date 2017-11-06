#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "knarfeh@outlook.com"

import logging
from ..utils.email.send_email import send_email

LOGGER = logging.getLogger(__name__)


class NotificationClient(object):
    def send_email(self, data):
        LOGGER.debug('Sending email with data: %s', data)
        send_email.delay(data)

