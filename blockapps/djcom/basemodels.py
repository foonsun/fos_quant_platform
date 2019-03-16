from django.db import models
import traceback
from json import dumps as jdumps, loads as jloads
from datetime import datetime
from django.utils.timezone import localtime
from django.utils.translation import ugettext as _

# --- Custom managers
class ActiveManager(models.Manager):
    def active(self):
        return super(ActiveManager, self).filter(is_active=True)

# --- Abstract classes
class MiscObjModel(models.Model):
    misc = models.TextField(verbose_name=(_('other fields with json format')),
                            null=True, blank=True)
    def set_miscobj(self, miscobj):
        self._miscobj = miscobj
        self.misc = jdumps(miscobj)

    def get_miscobj(self):
        miscobj = getattr(self, '_miscobj', None)
        if miscobj is not None: return self._miscobj
        if not self.misc: self._miscobj = {}
        else:
            try:
                self._miscobj = jloads(self.misc)
            except Exception as e:
                traceback.print_exc()
                self._miscobj = {}

        if type(self._miscobj) != dict:
            self._miscobj = {'miscobj': self._miscobj}
        return self._miscobj

    class Meta:
        abstract = True

class DatedModel(models.Model):
    creation_time = models.DateTimeField(default=datetime.now, db_index=True)
    modification_time = models.DateTimeField(auto_now=True, db_index=True)
    #modification_time.editable=True

    class Meta:
        abstract = True

    def modifyTimeStr(self):
        return localtime(self.modification_time).strftime('%Y%m%d %H:%M:%S')

    def createTimeStr(self):
        return localtime(self.modification_time).strftime('%Y%m%d %H:%M:%S')

class ActiveModel(models.Model):
    is_active = models.BooleanField(verbose_name=_('Is active?'), default=True, db_index=True)
    objects = ActiveManager()

    class Meta:
        abstract = True

class AbstractMessage(DatedModel):
    userid = models.IntegerField(db_index=True, verbose_name=_('Owner'))
    ctype = models.IntegerField(blank=True, null=True, verbose_name=_('Message Type'))
    to_userid = models.IntegerField(db_index=True, verbose_name=_('To User'))
    was_read = models.BooleanField(verbose_name=_('Was read?'), default=False)
    was_read_at = models.DateTimeField(editable=False, blank=True, null=True)
    topic = models.CharField(verbose_name=_('Topic'), max_length=200)
    message = models.TextField(verbose_name=_('Message'))

    class Meta:
        abstract = True

class AbstractLink(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length = 50)
    class Meta:
        abstract = True

class AbstractLog(models.Model):
    LEVEL_INFO = 0
    LEVEL_DEBUG = 1
    LEVEL_WARNING = 2
    LEVEL_ERROR = 3
    level = models.SmallIntegerField(db_index=True)
    userid = models.IntegerField()
    creation_time = models.DateTimeField(default=datetime.now)
    detail = models.CharField(max_length=200, verbose_name=_('log detail'),
                              null=True, blank=True)

    @classmethod
    def I(cls, userid, detail):
        cls(level=cls.LEVEL_INFO, userid=userid, detail=detail).save()
    @classmethod
    def D(cls, userid, detail):
        cls(level=cls.LEVEL_DEBUG, userid=userid, detail=detail).save()
    @classmethod
    def W(cls, userid, detail):
        cls(level=cls.LEVEL_WARNING, userid=userid, detail=detail).save()
    @classmethod
    def E(cls, userid, detail):
        cls(level=cls.LEVEL_ERROR, userid=userid, detail=detail).save()

    class Meta:
        abstract = True

