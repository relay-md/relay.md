# -*- coding: utf-8 -*-
# Instanciate Celery and configure it accordingly

from celery import Celery, Task

from .config import get_config
from .database import get_session


class BaseTask(Task):
    """Custom task class so we can more easily patch sessions in unittests.

    As per https://docs.celeryq.dev/en/latest/userguide/tasks.html#instantiation
    """

    #: This allows to inject a session in unittests
    _db = None

    #: Configure automatic retries

    # A list/tuple of exception classes. If any of these exceptions are raised
    # during the execution of the task, the task will automatically be retried.
    autoretry_for = ()

    # A number. Maximum number of retries before giving up. A value of None
    # means task will retry forever. By default, this option is set to 3.
    max_retries = 5

    # A boolean, or a number. If this option is set to True, autoretries will
    # be delayed following the rules of exponential backoff. The first retry
    # will have a delay of 1 second, the second retry will have a delay of 2
    # seconds, the third will delay 4 seconds, the fourth will delay 8 seconds,
    # and so on. (However, this delay value is modified by retry_jitter, if it
    # is enabled.) If this option is set to a number, it is used as a delay
    # factor. For example, if this option is set to 3, the first retry will
    # delay 3 seconds, the second will delay 6 seconds, the third will delay 12
    # seconds, the fourth will delay 24 seconds, and so on. By default, this
    # option is set to False, and autoretries will not be delayed.
    retry_backoff = True

    # A number. If retry_backoff is enabled, this option will set a maximum
    # delay in seconds between task autoretries. By default, this option is set
    # to 600, which is 10 minutes.
    retry_backoff_max = 600

    # A boolean. Jitter is used to introduce randomness into exponential
    # backoff delays, to prevent all tasks in the queue from being executed
    # simultaneously. If this option is set to True, the delay value calculated
    # by retry_backoff is treated as a maximum, and the actual delay value will
    # be a random number between zero and that maximum. By default, this option
    # is set to True.
    retry_jitter = True

    @property
    def name(self):
        """Class based tasks require a name"""
        return f"{self.__module__}: {self.__name__}"

    @property
    def db(self):
        """Allows to access a database session"""
        if self._db is None:
            self._db = next(get_session())
        return self._db

    def after_return(self, *args, **kwargs):
        """
        After running the task let's clean up
        """
        if self._db is not None:
            self._db.close()


class MyCelery(Celery):
    pass


celery = MyCelery(__name__)
celery.conf.update(get_config().CELERY_CONF.model_dump())
