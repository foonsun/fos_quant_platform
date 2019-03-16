from sys import stderr

def assertTrue(condition, msg=''):
    if not condition:
        if msg: stderr.write(msg)
        raise AssertionError(msg)
    
def assertFalse(condition, msg=''):
    if condition:
        if msg: stderr.write(msg)
        raise AssertionError(msg)

class TcBase(object):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def work(self, funcmatch=''):
        for key in dir(self):
            if not key.startswith('test_'): continue
            if funcmatch and not key.startswith(funcmatch): continue
            val = getattr(self, key)
            if not callable(val): continue
            self.setUp()
            print('--- method(%s) ---' % key)
            val()
            self.tearDown()

    def assertTrue(self, condition, msg):
        assertTrue(condition, msg)
    
    def assertFalse(self, condition, msg):
        assertFalse(condition, msg)
