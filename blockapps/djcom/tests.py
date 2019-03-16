import uuid
import unittest
from djcom.basemodels import MemModel
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime, time
from django.core.exceptions import ValidationError

class TestMemModel(MemModel):
    pkey = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='Title')
    content = models.TextField(blank=True, null=True)
    floatval = models.FloatField()
    urlval = models.URLField()
    boolval = models.BooleanField(default=False)
    bintval = models.BigIntegerField(verbose_name='BigIntegerField')
    dateval = models.DateField(default=datetime.today)
    dtval = models.DateTimeField(default=timezone.now)
    timeval = models.TimeField(default=time(16, 0))
    emailval = models.EmailField()
    pintval = models.PositiveIntegerField(default=200)
    psintval = models.PositiveSmallIntegerField()
    sintval = models.SmallIntegerField()
    uuidval = models.UUIDField(default=uuid.uuid4)
    
    def __str__(self):
        result = []
        for field in self._meta.local_fields:
            result.append('%s(%s)' % (field.name, getattr(self, field.name)))
        return ', '.join(result)
