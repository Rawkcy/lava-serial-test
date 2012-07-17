import time


class i2cTest(object):

    def __init__(self, conn):
        """
        Test COM's i2c bus communications
            - check that number of I2C buses is present
        """
        self.conn = conn

    def test_runner(self, cmd, response, timeout=5):
        """
        Wrapper to execute test cases
        """
        localResult = {}
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = cmd
        localResult['result'] = 'pass' if success else 'fail'
        return localResult


def run(conn):
    results = []

    i2c_test = i2cTest(conn)
    results.append(i2c_test.test_runner('i2cdetect -F 1', 'yes'))
    results.append(i2c_test.test_runner('i2cdetect -F 3', 'yes'))

    return results

