"""
Test suite run wrapper
"""

import time


class TestRunner(object):

    def __init__(self, conn):
        self.conn = conn

    def run(self, cmd, response, timeout=5):
        localResult = {}
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = '%s | %s' % (self.__class__.__name__, cmd)
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

