import os
from functools import wraps

from celery import Task

from nationbuilder_api import NationBuilderClient
from worker import queue


class BaseTask(Task):
    rate_limit = "24/m"
    time_limit = 30
    autoretry_for = (Exception,)


class CreateDiscountTask(BaseTask):
    max_retries = 2
    default_retry_delay = 10

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        with NationBuilderClient() as nb:
            nb.people.update({os.environ["SHOP_PENDING_FIELD"]: None}, args[0])


def lock(f):
    @wraps(f)
    def dec_f(*args, **kwargs):
        with queue.connection_or_acquire() as conn:
            with conn.default_channel.client.lock(f.__name__, 30, blocking_timeout=5):
                return f(*args, **kwargs)

    return dec_f
