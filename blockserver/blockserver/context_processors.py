from django.conf import settings

def templatevars(request):
    return {'SITE_DOMAIN': settings.SITE_DOMAIN,
            'SITE_URL': settings.SITE_URL,
            'SITE_NAME': settings.SITE_NAME,
            }
