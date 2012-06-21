#!/usr/bin/env python
# Mustafa Faraj (mustafa@gumstix.com)
# Roxanne Guo (roxanne@gumstix.com)

import os
import sys
import json
import argparse
import base64
from uuid import uuid4

import utils
import swprofile
import hwprofile
import bundle_edit
from conmux import ConmuxConnection


def main():
    """
    Parse out arguments
    """
    parser = argparse.ArgumentParser(description="Execute tests over a serial interface.")
    parser.add_argument('target', help='Conmux connection target board name')
    parser.add_argument('-d', '--results_dir', default=os.getcwd(), help='Bundle file directory')
    parser.add_argument('tests', help='Test suites', nargs='+')
    args = parser.parse_args()
    setUp(args.tests, args.target, args.results_dir)


def setUp(test_suites, target, result_dir):
    """
    Set up a conmux connection instance
    Execute and log the board start up sequence
    """
    conn = ConmuxConnection(target, result_dir)
    raw_input("Press <enter> then start the board.")
    if not conn.uBoot() or not conn.loginPrompt() or not conn.login():
        raw_input("Something has gone terribly wrong!\nPress <enter> to exit.")
        sys.exit(1)
    run(test_suites, result_dir, conn)


def run(test_definitions, result_dir, conn):
    """
    Execute each test_suite sequentially

    Each test suite should:
    - execute test
    - append to log file
    - append to "test_results" in bundle file

    NOTE: bundle format can be found at
        http://linaro-dashboard-bundle.readthedocs.org/en/latest/schema/docs.html
    """
    bundle = {
        'format': 'Dashboard Bundle Format 1.3',
        'test_runs': [
            {
            'test_id': 'tobi',
            'analyzer_assigned_uuid': str(uuid4()),
            'analyzer_assigned_date': '2010-11-14T13:42:31Z',
            'time_check_performed': False,
            'test_results':[],
            'attachments':[],
            'hardware_context': hwprofile.get_hardware_context(conn),
            'software_context': swprofile.get_software_context(conn)
            }
        ]
    }

    # Run test suites
    for test_definition in test_definitions:
        importpath = "lava_serial_test.test_definitions.%s" % test_definition
        try:
            test_definition = __import__(importpath)
        except ImportError:
            print "Unknown test '%s'" % test_definition
            continue
        try:
            # Grab the test file
            for mod in importpath.split('.')[1:]:
                test_definition = getattr(test_definition, mod)
        except AttributeError:
            print "Failed to find %s" % test_definition
        # Run and store each result
        test_result = test_definition.run(conn)
        bundle['test_runs'][0]['test_results'].extend(test_result)

    # TODO: don't like this code together in main .. should be its own function?
    logfile = os.path.join(conn.logDirectory, '%s.log' % conn.board)
    mime_type = 'text/plain'
    data = ''.join(utils.clean_and_return_log(conn))
    content = base64.standard_b64encode(data)
    bundle['test_runs'][0]['attachments'].extend(bundle_edit.add_attachments(conn, logfile, mime_type, content))

    # Dump bundle stream
    output = open(os.path.join(result_dir, '%s.json' % conn.board),'wb')
    json.dump(bundle, output, indent=2)
    output.close()


if __name__ == "__main__":
    main()
