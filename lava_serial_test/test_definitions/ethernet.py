"""
Ethernet test suite

`ifconfig` | view configured network interface info
`ping` | test whether a host is reachable across an IP network
`nslookup` | query Domain Name System (DNS)
`wget` | retrieve content from web server
`dmesg` | check for irq 336 in kernel boot
"""

from os.path import splitext, basename
from lava_serial_test.test_runner import TestRunner


def run(conn):
    results = []
    test_name = splitext(basename(__file__))[0]
    test_runner = TestRunner(conn, test_name)

    results.append(test_runner.run('ifconfig', 'eth[0-9]+'))
    results.append(test_runner.run('ping -c 4 8.8.8.8', '[0-9]+ received'))
    results.append(test_runner.run('nslookup cumulus.gumstix.org', '74.3.164.55', 10))
    results.append(test_runner.run('wget www.google.com', '200 OK', 20))
    results.append(test_runner.run('dmesg', 'irq 336'))

    return results

