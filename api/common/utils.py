#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid
import functools
import six
from flask import jsonify
from werkzeug.routing import BaseConverter


def generate_uuid():
   return str(uuid.uuid4())


def merge_dicts(*dict_args):
    """
    Given any number of dict, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def is_string(text):
    """
    :param text: input content
    check if the text is string type, return True if it is, else return False.
    """
    if six.PY2:
        return isinstance(text, basestring)
    return isinstance(text, (str, bytes))


def convert_to_unicode(text):
    """
    :param text: input content
    If text is utf8 encoded, then decode it with utf8 and return it, else just return it.
    """
    assert is_string(text), 'text must be string types.'

    try:
        return text.decode('utf-8')
    except UnicodeEncodeError:  # python2 will raise this exception when decode unicode.
        return text
    except AttributeError:  # python3 will raise this exception when decode unicode.
        return text


# Can be moved to a common package, Temporarily did not add a colored log
def get_log_config(component, handlers, level='DEBUG', path='/var/log/eebook'):
    """
    Return a log config.
    :param component: name of component
    :param handlers: debug, info, error
    :param level: the level of the log
    :param path: The path to the log
    :return: config for flask-logconfig
    """
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s][%(threadName)s]' +
                '[%(name)s.%(funcName)s():%(lineno)d] %(message)s'
            },
        },
        'handlers': {
            'debug': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': path + component + '.debug.log',
                'maxBytes': 1024 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'standard',
            },
            'info': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': path + component + '.info.log',
                'maxBytes': 1024 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'standard',
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': path + component + '.error.log',
                'maxBytes': 1024 * 1024 * 100,
                'backupCount': 5,
                'formatter': 'standard',
            },
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            'werkzeug': {
                'handlers': ['info', 'console'],
                'level': 'INFO',
                'propagate': False
            },
            # api can not be empty, not consistent with Django, if have time, maybe help fix this?
            'api': {
                'handlers': handlers,
                'level': level,
                'propagate': False
            },
            '': {
                'handlers': handlers,
                'level': level
            }
        }
    }
    return config


def json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        from .middleware.response import JSONResponse
        if isinstance(rv, JSONResponse):
            return rv
        status_or_headers = None
        headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None
        if not isinstance(rv, dict):
            rv = rv.to_json()
        rv = jsonify(rv)
        if status_or_headers is not None:
            rv.status_code = status_or_headers
        if headers is not None:
            rv.headers.extend(headers)
        return rv
    return wrapped


# Make Flask url support regular expression
# steal from https://stackoverflow.com/questions/5870188/does-flask-support-regular-expressions-in-its-url-routing
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
