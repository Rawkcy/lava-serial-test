"""
i2c test suite

`i2cdetect` | check that number of I2C buses is present
"""

from test_runner import TestRunner


def run(conn):
    results = []
    test_runner = TestRunner(conn)

    results.append(test_runner.run('i2cdetect -F 1', 'yes'))
    results.append(test_runner.run('i2cdetect -F 3', 'yes'))

    return results

