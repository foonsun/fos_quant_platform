from django.test import TestCase
from .tasks import add, run_limitbuy_policy
import time
# Create your tests here.
class CeleryTestCase(TestCase):
    def test_celery_high_concurrent(self):
        while True:
            time.sleep(1)
            run_limitbuy_policy.delay(47)