from celery import shared_task

from apps.digitizing.models import DigitizingJob
from apps.digitizing.services.workflow import process_job


@shared_task
def process_digitizing_job(job_id):
    job = DigitizingJob.objects.get(pk=job_id)

    process_job(job)