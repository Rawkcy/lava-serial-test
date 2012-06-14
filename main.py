#!/usr/bin/env python
# Author: Mustafa Faraj (vis.mustafa@gmail.com)
#
# This file is part of the Gumstix modification for the LAVA Dispatcher.
# This file contains all the tests that can run on any Gumstix Overo device.

import os
import sys
import json
import argparse

from conmux import ConmuxConnection
from profile import swprofile, hwprofile

#def is_ascii(s):
#    return all(ord(c) < 128 for c in s)

def setUp(test_suites, target, result_dir):
    conn = ConmuxConnection(target, result_dir)
    raw_input("Press <enter> then start the board.")
    if conn.logBootup():
        raw_input("Failed to boot up. Press <enter> to continue.")
    if conn.login():
        #failed to login to linux. cancel and return something else
        raw_input("Can not login to the board. Press <enter> to continue.")
    run(test_suites, result_dir, conn)

def run(test_suites, result_dir, conn):
    hw_profile = hwprofile.get_hardware_context(conn)
    sw_profile = swprofile.get_hardware_context(conn)
    bundle = {
        'format': 'LAVA Serial Test',
        'test_runs': []
    }
    bundle_template = {
        'analyzer_assigned_uuid': '',
        'analyzer_assigned_date': '',
        'time_check_performed': False,
        'attributes':{},
        'test_id': '',
        'test_results':[],
        'attachments':[],
        'hardware_context': hw_profile,
        'software_context': sw_profile
    }
    for test_suite in test_suites:
        # NOTE: this is how LAT does it
        #importpath = "lava_serial_test.test_suites.%s" % test_suite
        #test_suite = __import__(importpath)

        # Import python module from string
        try:
            test_suite = __import__(test_suite)
        except ImportError:
            print "unknown test '%s'" % test_suite
            sys.exit(1)
        # Run and store each result
        data = test_suite.run(bundle_template, conn)
        bundle['test_runs'].append(data)

    #cleanOut = ''
    #for line in rawOut.split('\n'):
    #    if is_ascii(line):
    #        cleanOut = cleanOut + line
    #    else:
    #        cleanOut = cleanOut + "##Non-Ascii characters were detected here##\n"

    output = open(os.path.join(result_dir,'results'),'wb')
    # Use json to pass results to lava-dispatch
    json.dump(bundle, output)
    output.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute tests over serial.")
    parser.add_argument('target', help='Conmux target name')
    parser.add_argument('-d', '--results_dir', default=os.getcwd(), help='Test results directory')
    parser.add_argument('tests', help='Test suites', nargs='+')
    args = parser.parse_args()
    setUp(args.tests, args.target, args.results_dir)
