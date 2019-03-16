from django.test.client import Client
from json import dumps as jdumps

class BaseJsonTestCaseMixin(object):
    def setUp(self):
        headers = getattr(self, 'headers', {})
        headers = self._uniformHeaders(headers)
        self.client = Client(**headers)

    def request(self, url, headers={}, data={}, method='post', content_type="application/json", withAssert=True):
        retobj = self._request(url, headers=headers, data=data, method=method,
            content_type=content_type, withAssert=withAssert)
        return retobj

    def _request(self, url, headers, data, method, content_type, withAssert):
        headers = self._uniformHeaders(headers)
        if method.lower() == 'get':
            res = self.client.get(url, content_type="application/json", **headers)
        elif method.lower() == 'post':
            res = self.client.post(url, jdumps(data), content_type="application/json", **headers)
        else:
            raise RuntimeError('unknown method(%s)' % method)
        if withAssert and res.status_code != 200:
            raise Exception('request %s failed-> %s' % (url, res.content))
        try:
            jobj = res.json()
            #print('request result: %s' % jdumps(jobj))
            return jobj
        except Exception as e:
            raise Exception('request %s failed with code %s' % (url, res.status_code))

    def _uniformHeaders(self, headers):
        result = {}
        for key, val in headers.items():
            key = key.lower()
            if not key.startswith('http_'):
                key = 'http_%s' % key
            result[key.upper()] = val
        return result
