# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.schedules import crontab
from blockserver import celery_app
from django.utils import timezone
from time import sleep
from blockuser.duiqiao import DuiQiao

@shared_task
def add(x, y):
    print(x,y)
    return x + y