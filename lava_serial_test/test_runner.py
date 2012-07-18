"""
Test suite run wrapper
"""

import time


class TestRunner(object):

    def __init__(self, conn, test_name):
        self.conn = conn
        self.test_name = test_name

    def run(self, cmd, response, timeout=5):
        localResult = {}
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = '%s | %s' % (self.test_name, cmd)
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

