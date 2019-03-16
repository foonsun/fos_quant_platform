import unittest
from blockdjcom.tcconfig import TcConfig
from djcom.basetc import BaseJsonTestCaseMixin

class BaseTc(unittest.TestCase):
    def setUp(self):
        self.ctx = TcConfig.CreateContext()
        super(BaseTc, self).setUp()

    def tearDown(self):
        pass

class BaseJsonTc(BaseJsonTestCaseMixin, unittest.TestCase):
    def setUp(self):
        ctx = TcConfig.CreateContext()
        self.headers = {'apikey': ctx.apikey, 'apisecret': ctx.apisecret}
        self.ctx = ctx
        BaseJsonTestCaseMixin.setUp(self)
        unittest.TestCase.setUp(self)

    def tearDown(self):
        pass
