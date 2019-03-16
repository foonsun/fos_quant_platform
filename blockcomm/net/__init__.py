class Retmsg():
    def __init__(self, ret=0, msg=''):
        self.ret = ret
        self.msg = msg

    def __bool__(self):
        return bool(self.ret)
    __nonzero__=__bool__

    def __str__(self):
        return self.msg
