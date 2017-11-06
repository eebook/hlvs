#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from api.common.utils import get_log_config


class Config(object):
    LOG_HANDLER = os.getenv('LOG_HANDLER', 'debug,info,error').split(',')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    LOG_PATH = os.getenv('LOG_PATH', '/var/log/eebook/')
    LOGCONFIG = get_log_config(component='hlvs', handlers=LOG_HANDLER, level=LOG_LEVEL, path=LOG_PATH)
    LOGCONFIG_QUEUE = ['eebook']
    USER_DEFAULT_LANGUAGE = 'en'
    PAGINATE_BY = os.getenv('PAGINATE_BY', 10)
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True

    HLVS_HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'HLVS/v1.0'
    }

    SMTP = {
        'server': os.getenv('SMTP_SERVER_HOST', 'smtp.qq.com'),
        'port': os.getenv('SMTP_SERVER_PORT', 465),
        'username': os.getenv('SMTP_USERNAME', '2559775198@qq.com'),
        'password': os.getenv('SMTP_PASSWORD'),
        'sender': os.getenv('EMAIL_FROM', '2559775198@qq.com'),
        'debug_level': 0,
    }

    EMAIL_CONFIG = {
        'template_path': 'email',
        'sender': os.getenv('EMAIL_FROM', '2559775198@qq.com'),
        'debug_cc_email': 'knarfeh@outlook.com',
        'eebook_url': os.getenv('EEBOOK_URL') or 'https://www.eebook.com',
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    LOG_HANDLER = os.getenv('LOG_HANDLER', 'debug,info,error').split(',')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_PATH = os.getenv('LOG_PATH', '/var/log/eebook/')
    LOGCONFIG = get_log_config(component='hlvs', handlers=LOG_HANDLER, level=LOG_LEVEL, path=LOG_PATH)


config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}
