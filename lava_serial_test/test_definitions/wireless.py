"""
Bluetooth and Wifi test suite

`ifconfig` | check that Wifi is found
`hciconfig` | check that Bluetooth is found
`dmesg` | check that Wi2Wi Transceiver is found
"""

import os
from lava_serial_test.test_runner import TestRunner


def run(conn):
    results = []
    test_name = os.path.basename(__file__)
    test_runner = TestRunner(conn, test_name)

    results.append(test_runner.run('ifconfig', 'wlan[0-9]'))
    results.append(test_runner.run('hciconfig', 'hci0'))
    results.append(test_runner.run('dmesg', 'libertas'))

    return results

