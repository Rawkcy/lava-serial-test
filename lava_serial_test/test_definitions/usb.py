"""
USB test suite

`lsusb` | check if USB host detected
`lsusb` | check if USB OTG port detected
`lsusb` | check if console port detected
`evtest` | keyboard test
`evtest` | mouse test
"""

from test_runner import TestRunner


def run(conn):
    results = []
    test_runner = TestRunner(conn)

    results.append(test_runner.run('lsusb', 'Bus 001 Device 00[2-9]'))
    results.append(test_runner.run('lsusb', 'Bus 002 Device 00[2-9]'))
    results.append(test_runner.run('lsusb', 'Future'))
    #NOTE: requires evtest to be installed
    # USB keyboard
    #results.append(usb_test.test_runner('evtest /dev/input/event2', 'Future'))
    # USB mouse
    #results.append(usb_test.test_runner('evtest /dev/input/event4', 'Future'))

    return results

