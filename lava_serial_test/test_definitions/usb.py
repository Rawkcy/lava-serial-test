import time

class UsbTest(object):

    def __init__(self, conn):
        """
        Tests the board's USB connections by
            - check we have right amount of USB ports
            -
            -
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

    usb_test = UsbTest(conn)
    results.append(usb_test.test_runner('lsusb', 'Bus 001 Device 00[2-9]'))

    return results
