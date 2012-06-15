import time

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
        localResult['test_case_id']= 'ifconfig'
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
        localResult['test_case_id']= 'ping'
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
        localResult['test_case_id']= 'nslookup'
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
        localResult['test_case_id']= 'wget'
        localResult['result'] = 'pass' if success else 'fail'
        return localResult


def run(conn):
    results = []
    ethernet_test = ethernet(conn)

    result = ethernet_test.ifconfig()
    results.append(result)
    result = ethernet_test.ping()
    results.append(result)
    result = ethernet_test.nslookup()
    results.append(result)
    result = ethernet_test.wget(20)
    results.append(result)

    return results