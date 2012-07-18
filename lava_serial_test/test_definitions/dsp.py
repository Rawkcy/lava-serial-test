"""
Digital Signal Processor (DSP) test suite

`[ -e /dev/dsp ]` | check if DSP is found
"""

import os
from lava_serial_test.test_runner import TestRunner


def run(conn):
    results = []
    test_name = os.path.basename(__file__)
    test_runner = TestRunner(conn, test_name)

    results.append(test_runner.run('[ -e /dev/dsp ] && echo "pass" || echo "fail"', 'pass'))

    return results

