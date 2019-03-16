import re
import socket
from django.utils import timezone
from django.contrib import admin
from django.db.models.base import ModelBase
from django.contrib.admin.sites import AlreadyRegistered

def registerAdminFromModels(models, excludePatterns=[]):
    for name, modelcls in models.__dict__.items():
        if type(modelcls) is ModelBase:
            if modelcls._meta.abstract == True:
                continue
            try:
                matched = False
                for pattern in excludePatterns:
                    if re.match(pattern, modelcls.__name__):
                        matched = True
                if matched:
                    #print('exclude model %s' % modelcls.__name__)
                    continue
                admin.site.register(modelcls)
            except AlreadyRegistered as e:
                pass

def dt1970():
    return timezone.datetime(1970, 1, 1, tzinfo=timezone.utc)

def ts2dt(ts):
    if not ts: ts = 0
    ts = int(ts)
    if ts > (9999999999):
        ts = int(ts/1000)
    return timezone.datetime.utcfromtimestamp(ts).replace(tzinfo=timezone.utc)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_server_ip(request):
    try:
        ip = socket.gethostbyname(request.META['SERVER_NAME'])
        return ip
    except socket.gaierror as e:
        return '127.0.0.1'
