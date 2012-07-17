import time


class TestRunner(object):

    def __init__(self, conn):
        """
        Wrapper to execute test cases
        """
        self.conn = conn

    def run(self, cmd, response, timeout=5):
        localResult = {}
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = cmd
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

