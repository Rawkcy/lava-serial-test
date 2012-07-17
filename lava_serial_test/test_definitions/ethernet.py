import time


class EthernetTest(object):

    def __init__(self, conn):
        """
        Tests the board's ethernet connectivity
            - `ifconfig` | view configured network interface info
            - `ping` | test whether a host is reachable across an IP network
            - `nslookup` | query Domain Name System (DNS)
            - `wget` | retrieve content from web server
            - `dmesg` | check for irq 336 in kernel boot
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

    ethernet_test = EthernetTest(conn)
    results.append(ethernet_test.test_runner('ifconfig', 'eth[0-9]+'))
    results.append(ethernet_test.test_runner('ping -c 4 8.8.8.8', '[0-9]+ received'))
    results.append(ethernet_test.test_runner('nslookup cumulus.gumstix.org', '74.3.164.55', 10))
    results.append(ethernet_test.test_runner('wget www.google.com', '200 OK', 20))
    results.append(ethernet_test.test_runner('dmesg', 'irq 336'))

    return results

