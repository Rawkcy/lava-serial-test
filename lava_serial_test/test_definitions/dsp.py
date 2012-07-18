"""
Digital Signal Processor (DSP) test suite

`[ -e /dev/dsp ]` | check if DSP is found
"""

from os.path import splitext, basename
from lava_serial_test.test_runner import TestRunner


def run(conn):
    results = []
    test_name = splitext(basename(__file__))
    test_runner = TestRunner(conn, test_name)

    results.append(test_runner.run('[ -e /dev/dsp ] && echo "pass" || echo "fail"', 'pass'))

    return results

