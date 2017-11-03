#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import logging
from werkzeug.exceptions import HTTPException, default_exceptions
from flask import Flask, Blueprint, request, jsonify
from flask_logconfig import LogConfig


from config import config
from .common.exceptions import APIException
from .common.middleware import response
from .common.utils import RegexConverter


BP_NAME = 'root'
root_bp = Blueprint(BP_NAME, __name__)
LOGGER = logging.getLogger(__name__)


@root_bp.route("/_ping", methods=["GET"])
def ping():
    return "pong\n"


def create_app(config_name='dev'):
    app = Flask(__name__)

    # IN
    @app.before_request
    def ensure_content_type():
        content_type = request.headers.get('Content-type')
        if not content_type == 'application/json':
            raise APIException('invalid_content_type')
    # OUT
    app.response_class = response.JSONResponse

    # def make_json_error(ex):
    #     res = jsonify(message=str(ex))
    #     res.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    #     return res
    #
    # for code in default_exceptions.keys():
    #     app.error_handler_spec[None][code] = make_json_error

    response.json_error_handler(app=app)

    # Load default configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    logcfg = LogConfig(app)
    logcfg.init_app(app)

    # Support regular expression
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(root_bp, url_prefix='/v1')

    from .courier import courier_bp
    app.register_blueprint(courier_bp, url_prefix='/v1/email')

    return app
