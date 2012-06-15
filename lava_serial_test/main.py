#!/usr/bin/env python
# Mustafa Faraj (vis.mustafa@gmail.com)
# Roxanne Guo (roxane.guo@gmail.com)

import os
import sys
import json
import argparse
from uuid import uuid4

import swprofile
import hwprofile
from conmux import ConmuxConnection


#def is_ascii(s):
#    return all(ord(c) < 128 for c in s)

def setUp(test_suites, target, result_dir):
    """
    Set up a conmux connection instance
    Execute and log the board start up sequence
    """
    conn = ConmuxConnection(target)
    raw_input("Press <enter> then start the board.")
    if not conn.uBoot() or not conn.loginPrompt() or not conn.login():
        raw_input("\nPress <enter> to exit.")
        sys.exit(1)
    run(test_suites, result_dir, conn)


def run(test_definitions, result_dir, conn):
    """
    Execute each test_suite sequentially

    Each test suite should:
    - execute test
    - append to log file
    - append to "test_results" in bundle file
    """
    #hw_profile = hwprofile.get_hardware_context(conn)
    #sw_profile = swprofile.get_hardware_context(conn)
    #tmp_path = '/tmp/test.txt'
    #with open(tmp_path, 'rb') as stream:
    #    data = stream.read()
    bundle = {
        'format': 'Dashboard Bundle Format 1.3',
        'test_runs': [
            {
            'test_id': 'stream',
            'analyzer_assigned_uuid': str(uuid4()),
            'analyzer_assigned_date': '2010-11-14T13:42:31Z',
            'time_check_performed': False,
            #'attributes':{},
            'test_id': 'example',
            'test_results':[],
            'attachments':[
                #{
                #    'pathname': '/tmp/test.txt',
                #    'mime_type': 'text/plain',
                #    'content': base64.standard_b64encode(data)
                #}
            ],
            #'hardware_context': '',#hw_profile,
            #'software_context': ''#sw_profile
            }
        ]
    }
    test_result_template = {
        'measurement': '',
        #'command': '',
        #'response': '',
        'message': '',
        'test_case_id': '',
        'result': ''
    }

    # Run test suites
    for test_definition in test_definitions:
        #importpath = "lava_serial_test.test_definitions.%s" % test_definition
        #test_definition = __import__(importpath)
        try:
            test_definition = __import__(test_definition)
        except ImportError:
            print "unknown test '%s'" % test_definition
            sys.exit(1)
        # Run and store each result
        test_result = test_definition.run(test_result_template, conn)
        bundle['test_runs'][0]['test_results'].append(test_result)

    #cleanOut = ''
    #for line in rawOut.split('\n'):
    #    if is_ascii(line):
    #        cleanOut = cleanOut + line
    #    else:
    #        cleanOut = cleanOut + "##Non-Ascii characters were detected here##\n"

    # Store bundle file and close pexpect instance
    output = open(os.path.join(result_dir, '%s.json' % conn.board),'wb')
    json.dump(bundle, output, indent=2)
    output.close()
    conn.proc.close()


if __name__ == "__main__":
    """
    Parse out arguments passed from cmd_lava_serial_test
    """
    parser = argparse.ArgumentParser(description="Execute tests over a serial interface.")
    parser.add_argument('target', help='Conmux connection target board name')
    parser.add_argument('-d', '--results_dir', default=os.getcwd(), help='Bundle file directory')
    parser.add_argument('tests', help='Test suites', nargs='+')
    args = parser.parse_args()
    setUp(args.tests, args.target, args.results_dir)
