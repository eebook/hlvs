from __future__ import absolute_import
from __future__ import unicode_literals

__author__ = "knarfeh@outlook.com"

from celery import Celery
from config import Config

celery_app = Celery('hlvs', broker=Config.CELERY_BROKER_URL, include=['api.utils.email.send_email'])
celery_app.conf.update({
    'namespace': 'CELERY',
    'CELERY_RESULE_BACKEND': Config.CELERY_RESULT_BACKEND,
    'CELERY_TASK_SERIALIZER': Config.CELERY_TASK_SERIALIZER,
    'CELERY_ACCEPT_CONTENT': Config.CELERY_ACCEPT_CONTENT,
    'CELERY_RESULT_SERIALIZER': Config.CELERY_RESULT_SERIALIZER,
    'CELERY_TIMEZONE': Config.CELERY_TIMEZONE,
    'CELERY_ENABLE_UTC': Config.CELERY_TIMEZONE
})
