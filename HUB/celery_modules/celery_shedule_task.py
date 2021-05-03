import logging
import signal

import celery

logger = logging.getLogger(__name__)


class Task(celery.Task):
    def __call__(self, *args, **kwargs):
        signal.signal(signal.SIGTERM,
                      lambda signum, frame: logger.info('SIGTERM received, wait till the task finished'))
        return super().__call__(*args, **kwargs)


class ScheduleTask(Task):
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        from HUB.caches.cache_utils import delete_cached_object
        prefixed_task_name = self.get_prefixed_name()
        delete_cached_object(prefixed_task_name)

    def get_prefixed_name(self):
        return "__celery__task__{}".format(self.name)


def decorate_app_schedule_task(app):
    def wrapper(*args, **kwargs):
        return app.task(base=ScheduleTask, *args, **kwargs)

    return wrapper
