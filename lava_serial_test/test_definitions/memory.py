import time


class MemoryTest(object):

    def __init__(self, conn):
        """
        Tests the board's memory unit by
            - creating half a gig sized file
            - matching the md5sum value
        """
        self.conn = conn

    # TODO: specific file generation parameters?
    def randomFileGen(self, timeout=5):
        """
        Generate file of randomness with given size
        """
        localResult = {}
        cmd = 'dd if=/dev/zero of=/home/root/MemoryTest count=1024 bs=1024'
        response = '1048576 bytes'
        result, success = self.conn.execute(cmd, response, timeout)
        startTime = time.time()
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = self.randomFileGen.__name__
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

    # NOTE: suppress the output?
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
        localResult['test_case_id'] = self.md5sumer.__name__
        localResult['result'] = 'pass' if success else 'fail'
        return localResult


# TODO(rox): count should be passed in through job file
def run(conn, count=100):
    results = []

    memory_test = MemoryTest(conn)
    results.append(memory_test.randomFileGen(100))
    results.append(memory_test.md5sumer(count))

    return results

