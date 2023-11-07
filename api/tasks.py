# -*- coding: utf-8 -*-
""" Async tasks as they are process by celery workers
"""
from celery.utils.log import get_task_logger
from .worker import BaseTask, celery


log = get_task_logger(__name__)


@celery.task(base=BaseTask, bind=True)
def hello():
    log.info("hello")
