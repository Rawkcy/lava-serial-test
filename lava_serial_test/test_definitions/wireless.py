import time


class WirelessTest(object):

    def __init__(self, conn):
        """
        Tests the board's bluetooth and wifi functionalities
            - `dmesg` | check that Wi2Wi Transceiver is found
            - `ifconfig` | check that Wifi is found
            - `ping` | check that Bluetooth is found
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
        localResult['test_case_id'] = '%s | %s' % (self.__class__.__name__, cmd)
        localResult['result'] = 'pass' if success else 'fail'
        return localResult


def run(conn):
    results = []

    wireless_test = WirlessTest(conn)
    results.append(wireless_test.test_runner('dmesg', 'libertas'))
    results.append(wireless_test.test_runner('ifconfig', 'wlan[0-9]'))
    results.append(wireless_test.test_runner('hciconfig', 'hci0'))

    return results

