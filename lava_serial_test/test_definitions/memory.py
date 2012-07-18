"""
Memory test suite

`dd` | create half a gig sized file
`md5sum` | match the md5sum value
"""

import time
from os.path import splitext, basename

from lava_serial_test.test_runner import TestRunner


class MemoryTest(object):

    def __init__(self, conn):
        self.conn = conn

    # NOTE: suppress the bajillion outputs?
    def md5sumer(self, count, timeout=5):
        """
        Successively recalculate the md5sum and compares correctness
        """
        localResult = {}
        cmd = 'md5sum /home/root/MemoryTest'
        return_code, result = self.conn.get_shellcmdoutput(cmd, timeout)
        success = True if return_code == 0 else False

        org_count = count
        while success and count:
            result, success = self.conn.execute(cmd, result, timeout)
            result = result.split('\n').pop()
            count -= 1
        failMsg = '' if success else 'WARNING: Memory stress test failed after %d iterations' % (org_count - count)

        startTime = time.time()
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = '%s %s' % (result, failMsg)
        localResult['test_case_id'] = '%s | %s' % (self.__class__.__name__, cmd)
        localResult['result'] = 'pass' if success else 'fail'
        return localResult


# TODO(rox): count could be passed in through job file
def run(conn, count=100):
    results = []
    test_name = splitext(basename(__file__))
    test_runner = TestRunner(conn, test_name)
    memory_test = MemoryTest(conn)

    results.append(test_runner.run('dd if=/dev/zero of=/home/root/MemoryTest count=1024 bs=1024', '1048576 bytes', 100))
    results.append(memory_test.md5sumer(count))

    return results

