# Mustafa Faraj (mustafa@gumstix.com)
# Roxanne Guo (roxanne@gumstix.com)

import os
from lava_dispatcher.actions import BaseAction


class cmd_lava_serial_test(BaseAction):
    """
    Calls lava-serial-test passing in test suites to be executed
    """

    parameters_schema = False
    @classmethod
    def validate_parameters(cls, parameters):
        super(cmd_lava_serial_test, cls).validate_parameters(parameters)

    def report_id(self, identity):
        """
        Print board information to screen
        """
        print "\n=======Operation Information======\n%s" % identity

    def run(self, identity, tests):
        """
        Need to parse out individual tests
        """
        target = self.context.job_data['target']
        result_dir = self.context.host_result_dir
        self.report_id(identity)
        #self.context.test_data.add_metadata(identity)

        # Do not try to make list into string if there is only one test
        test_definitions = ' '.join(tests) if len(tests) > 1 else tests[0]
        cmd = 'lava-serial-test %s -d %s %s' % (target, result_dir, test_definitions)
        os.system(cmd)
