from celery import Celery
from time import sleep
import datetime
import pytz
from django.core.mail import send_mail
from djangoproject.settings import EMAIL_HOST_USER
from django_celery_beat.models import CrontabSchedule, PeriodicTask
app = Celery(broker='redis://localhost:6379')

@app.task
def sleepy(msg,remainder):
        tz = pytz.timezone('Asia/Kolkata')
        d = datetime.datetime.now(tz)
        print("hello world")
        # send_mail("mail_subject", msg, EMAIL_HOST_US,
        # [divyavanakuri49@gmail.com], fail_silently=False,)
        return None

# schedule, _ =  CrontabSchedule.objects.get_or_create(
#         minute='*',
#         hour='*',
#         day_of_week='*',
#         day_of_month='*',
#         month_of_year='*',
#         timezone = pytz.timezone('Asia/Kolkata'),
# )
# PeriodicTask.objects.create(
#         crontab=schedule,
#         name='1267',
#         task='fundooappnote.tasks',
# )