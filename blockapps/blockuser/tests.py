from django.test import TestCase
from .tasks import add, run_duiqiao_policy
import time
# Create your tests here.
class CeleryTestCase(TestCase):
    def test_celery_high_concurrent(self):
        while True:
            time.sleep(1)
            run_duiqiao_policy.delay(47)