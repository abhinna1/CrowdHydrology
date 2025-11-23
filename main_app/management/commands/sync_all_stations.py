import django_rq
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_rq.queues import DjangoScheduler
from loguru import logger

from workers.tasks import generateStationCsvTask


class Command(BaseCommand):
    help = "Sets up periodic tasks using RQ Scheduler"

    def add_arguments(self, parser):
        parser.add_argument("dir", type=str, help="Directory to save CSV files.")
        parser.add_argument(
            "interval", type=int, help="Interval in minutes to run sync CRON."
        )

    def handle(self, *args, **options):
        scheduler: DjangoScheduler = django_rq.get_scheduler()
        save_directory, interval_minutes = options["dir"], options["interval"]

        # 1. Clear any old jobs with the same function to prevent duplicates
        # for job in scheduler.get_jobs():
        #     if job.func == daily_data_sync_to_cuahsi:
        #         scheduler.cancel(job)

        print(type(scheduler))

        # schedule cron job
        # cron.register(
        #     generateStationCsvTask,
        #     queue_name="default",
        #     interval=interval_minutes  # schedule in seconds.
        # )
        logger.info("Scheduling job.")
        scheduler.schedule(
            scheduled_time=timezone.now(),
            func=generateStationCsvTask,
            args=[save_directory],
            interval=interval_minutes,
            repeat=None,
            queue_name="default",
        )
        logger.info("Scheduled job.")
