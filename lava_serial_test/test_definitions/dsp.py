"""
Digital Signal Processor (DSP) test suite

`[ -e /dev/dsp ]` | check if DSP is found
"""

from test_runner import TestRunner


def run(conn):
    results = []
    test_runner = TestRunner(conn)

    results.append(test_runner.run('[ -e /dev/dsp ] && echo "pass" || echo "fail"', 'pass'))

    return results

