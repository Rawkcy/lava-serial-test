import time


class ethernet(object):

    def __init__(self, conn):
        """
        Ethernet test suite
        """
        self.conn = conn

    def test_runner(self, cmd, response, timeout=5):
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
    test_cases = ['ifconfig', 'ping', 'nslookup', 'wget']

    ethernet_test = ethernet(conn)
    for test_case in test_cases:
        results.append(ethernet_test.test_runner('ifconfig', 'eth[0-9]+'))
        results.append(ethernet_test.test_runner('ping -c 4 8.8.8.8', '[0-9]+ received'))
        results.append(ethernet_test.test_runner('nslookup cumulus.gumstix.org', '74.3.164.55', 10))
        results.append(ethernet_test.test_runner('wget www.google.com', '200 OK', 20))

    return results
