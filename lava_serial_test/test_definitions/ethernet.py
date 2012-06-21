import time

# TODO: render the escaped characters in result?
class ethernet():

    def __init__(self, conn):
        """
        Ethernet test suite
        """
        self.conn = conn

    def ifconfig(self, timeout=5):
        localResult = {}
        cmd = 'ifconfig'
        response = 'eth[0-9]+'
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        # trying to return function name: is there a point to this?
        localResult['test_case_id'] = self.ifconfig.__name__
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

    def ping(self, timeout=5):
        localResult = {}
        cmd = 'ping -c 4 8.8.8.8'
        response = '[0-9]+ received'
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = self.ping.__name__
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

    def nslookup(self, timeout=5):
        localResult = {}
        cmd = 'nslookup cumulus.gumstix.org'
        response = '74.3.164.55'
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = self.nslookup.__name__
        localResult['result'] = 'pass' if success else 'fail'
        return localResult

    def wget(self, timeout=5):
        localResult = {}
        cmd = 'wget www.google.com'
        response = '200 OK'
        startTime = time.time()
        result, success = self.conn.execute(cmd, response, timeout)
        localResult['measurement'] = time.time() - startTime
        localResult['message'] = result
        localResult['test_case_id'] = self.wget.__name__
        localResult['result'] = 'pass' if success else 'fail'
        return localResult


def run(conn):
    results = []
    ethernet_test = ethernet(conn)

    results.append(ethernet_test.ifconfig())
    results.append(ethernet_test.ping())
    results.append(ethernet_test.nslookup(10))
    results.append(ethernet_test.wget(20))

    return results
