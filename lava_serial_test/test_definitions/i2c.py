"""
i2c test suite

`i2cdetect` | check that number of I2C buses is present
"""

from os.path import splitext, basename
from lava_serial_test.test_runner import TestRunner


def run(conn):
    results = []
    test_name = splitext(basename(__file__))
    test_runner = TestRunner(conn, test_name)

    results.append(test_runner.run('i2cdetect -F 1', 'yes'))
    results.append(test_runner.run('i2cdetect -F 3', 'yes'))

    return results

