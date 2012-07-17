import time


class DspTest(object):

    def __init__(self, conn):
        """
        Test COM's Digital Signal Processor (DSP)
            - check if DSP is found
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
    results.append(ethernet_test.test_runner('[ -e /dev/dsp ] && echo "pass" || echo "fail"', 'pass'))

    return results

