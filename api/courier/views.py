#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import uuid
from flask import request

from ..common.utils import json
from ..common.exceptions import FieldValidateFailed
from ..common import status
from . import courier_bp
from .clients import NotificationClient

LOGGER = logging.getLogger(__name__)


@courier_bp.route('', methods=["POST"])
@json
def send_message():
    data = request.json
    NotificationClient().send_email(data)
    return {}, status.HTTP_204_NO_CONTENT


