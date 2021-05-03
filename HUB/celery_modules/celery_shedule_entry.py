from celery.beat import ScheduleEntry

from HUB.celery_modules.celery_shedule_task import ScheduleTask


class CeleryScheduleEntry(ScheduleEntry):
    def get_prefixed_task_name(self):
        task_obj = self.schedule.app.tasks.get(self.task)
        if isinstance(task_obj, ScheduleTask):
            prefixed_task_name = task_obj.get_prefixed_name()
            return prefixed_task_name
        raise NotImplementedError
