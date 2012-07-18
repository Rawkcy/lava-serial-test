"""
Bluetooth and Wifi test suite

`ifconfig` | check that Wifi is found
`hciconfig` | check that Bluetooth is found
`dmesg` | check that Wi2Wi Transceiver is found
"""

from test_runner import TestRunner


def run(conn):
    results = []
    test_runner = TestRunner(conn)

    results.append(test_runner.run('ifconfig', 'wlan[0-9]'))
    results.append(test_runner.run('hciconfig', 'hci0'))
    results.append(test_runner.run('dmesg', 'libertas'))

    return results

