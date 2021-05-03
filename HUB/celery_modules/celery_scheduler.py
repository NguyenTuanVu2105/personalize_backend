import heapq
import logging
import copy

from celery.beat import PersistentScheduler
from celery.schedules import schedstate
from celery.beat import event_t
from HUB.celery_modules.celery_shedule_entry import CeleryScheduleEntry
from helper.leader_election import is_master

DEFAULT_DELAY_IF_NOT_MASTER = 10

logger = logging.getLogger(__name__)


class CustomPersistentScheduler(PersistentScheduler):
    Entry = CeleryScheduleEntry

    def tick(self, event_t=event_t, min=min, heappop=heapq.heappop,
             heappush=heapq.heappush):
        """Run a tick - one iteration of the scheduler.

        Executes one due task per call.

        Returns:
            float: preferred delay in seconds for next call.
        """

        if not is_master():
            logger.info("I'M NOT MASTER SO I CANNOT SCHEDULE TASKS")
            return DEFAULT_DELAY_IF_NOT_MASTER

        adjust = self.adjust
        max_interval = self.max_interval

        if (self._heap is None or
                not self.schedules_equal(self.old_schedulers, self.schedule)):
            self.old_schedulers = copy.copy(self.schedule)
            self.populate_heap()

        H = self._heap

        if not H:
            return 0.5

        event = H[0]
        entry = event[2]
        is_due, next_time_to_run = self.is_due(entry)

        verify = heappop(H)
        if verify is event:
            if not is_due:
                # if worker still running on previous scheduled task
                # delay and recheck is_due after "next_time_to_run" seconds
                delayed_verify = list(verify)
                delayed_verify[0] = self._when(entry, next_time_to_run)
                delayed_verify = tuple(delayed_verify)
                heappush(H, delayed_verify)

                return 0.5
                # new_first_event = H[0]
                # new_is_due, new_next_time_to_run = new_first_event[2].is_due()
                # if new_is_due:
                #     return 0
                # return min(adjust(new_next_time_to_run) or max_interval, max_interval)
            else:
                next_entry = self.reserve(entry)
                self.apply_entry(entry, producer=self.producer)
                heappush(H, event_t(self._when(next_entry, next_time_to_run),
                                    event[1], next_entry))
                return 0
        else:
            heappush(H, verify)
            return 0.5

    def setup_schedule(self):
        super().setup_schedule()
        if is_master():
            self.run_all_entries_once_on_first_load()

    def run_all_entries_once_on_first_load(self):
        entries = self._store[str('entries')]
        for signature, entry in entries.items():
            if "celery.backend_cleanup" in signature:
                continue
            if not self.is_previous_entry_task_completed(entry=entry):
                continue
            self.apply_entry(entry)

    def is_due(self, entry):
        if not self.is_previous_entry_task_completed(entry=entry):
            return schedstate(is_due=False, next=1)
        return super().is_due(entry)

    def apply_entry(self, entry, *args, **kwargs):
        super().apply_entry(*args, entry=entry, **kwargs)
        self.mark_entry_task_as_applied(entry=entry)

    @staticmethod
    def is_previous_entry_task_completed(entry):
        from HUB.caches import get_cached_object
        prefixed_task_name = entry.get_prefixed_task_name()
        entry = get_cached_object(prefixed_task_name, decompress=False)
        if not entry:
            return True
        return False

    @staticmethod
    def mark_entry_task_as_applied(entry):
        from HUB.caches import cache_object
        prefixed_task_name = entry.get_prefixed_task_name()
        flag = '1'
        cache_object(obj=flag, cache_key=prefixed_task_name, timeout=600, compress=False)
