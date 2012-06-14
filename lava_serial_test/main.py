# Mustafa Faraj (vis.mustafa@gmail.com)
# Roxanne Guo (roxane.guo@gmail.com)

import os
import sys
import json
import argparse
import swprofile, hwprofile

from conmux import ConmuxConnection

#def is_ascii(s):
#    return all(ord(c) < 128 for c in s)

def setUp(test_suites, target, result_dir):
    """
    Set up a conmux connection instance, execute and log the board start up sequence
    """
    conn = ConmuxConnection(target)
    raw_input("Press <enter> then start the board.")
    if not conn.uBoot() or not conn.loginPrompt() or not conn.login():
        raw_input("Press <enter> to exit.")
        sys.exit(1)
    run(test_suites, result_dir, conn)

def run(test_suites, result_dir, conn):
    """
    Execute each test_suite sequentially

    Each test suite should:
    - execute test
    - append to log file
    - append to "test_results" in bundle file
    """
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
    """
    Parse out arguments passed from cmd_lava_serial_test
    """
    parser = argparse.ArgumentParser(description="Execute tests over a serial interface.")
    parser.add_argument('target', help='Conmux connection target board name')
    parser.add_argument('-d', '--results_dir', default=os.getcwd(), help='Bundle file directory')
    parser.add_argument('tests', help='Test suites', nargs='+')
    args = parser.parse_args()
    setUp(args.tests, args.target, args.results_dir)
