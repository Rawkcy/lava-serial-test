import time


class memoryStress(object):

    def __init__(self, conn):
        """
        Memory stress test suite
        """
        self.conn = conn

    # TODO: do we always want to fail?
    def md5sumer(self, mdsum, timeout=5):
        success = True
        count = 0
        while success:
            result, success = self.conn.execute(cmd, mdsum, timeout)
            count += 1

        localResult = {}
        cmd = 'md5sum /home/root/testfile'
        startTime = time.time()
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = 'Memory stress test failed after %d iterations.\n The shell output is %s' % (count, result)
        localResult['test_case_id'] = self.md5sumer.__name__
        # will always be fail
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

def run(conn):
    """
    Pass test case the correct mdsum test value
    """
    results = []
    memoryStress_test = memoryStress(conn)

    results.append(ethernet_test.md5sumer(mdsum))

    return results
