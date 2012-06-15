# Mustafa Faraj (mustafa@gumstix.com)
# Roxanne Guo (roxanne@gumstix.com

import tempfile
import pexpect
import os


# TODO: conmux connection sometimes requires reset
class ConmuxConnection():

    def __init__(self, board, result_dir):
        """
        Creates a conmux connection instance for testing over serial

        NOTE::
            The log file goes into /tmp/***_logs regardless of what
            directory path is passed into lava-serial-test
        """
        self.board = board
        self.promptString = ''
        if result_dir == os.getcwd():
            logfile = file(os.path.join(os.getcwd(), self.board + '.log'), 'w+r')
        else:
            logDirectory = result_dir + '_logs'
            if not os.path.exists(logDirectory):
                os.makedirs(logDirectory)
            logfile = file(os.path.join(logDirectory, self.board), 'w+r')
        self.proc = pexpect.spawn("conmux-console %s" % self.board, timeout=240)
        self.proc.logfile_read = logfile
        self.proc.setecho(False)


    def expectTry(self, cmdToSend, stringToExpect, timeOut):
        """
        Modular function used to singularly execute a command and
        expect an output
        """
        cmd_passed = True
        if cmdToSend:
            self.proc.sendline(cmdToSend)
        try:
            self.proc.expect(stringToExpect, timeout=timeOut)
        except pexpect.TIMEOUT:
            print "Command '%s' timed out" % cmdToSend
            print "Failed to match with '%s'" % stringToExpect
            cmd_passed = False
        return cmd_passed


    def uBoot(self):
        """
        First "test suite" to be executed
        Begins the log file by loggin uBoot sequence
        """
        test_passed = True
        if self.expectTry(" ", "Starting kernel", 45):
            print "##Sucessfully executed uBoot##"
        else:
            print "##Failed to execute uBoot => no tests will be ran on this device##\n"
            test_passed = False
        return test_passed


    def loginPrompt(self):
        """
        Test to see if we are prompted to login
        If so then we know uBoot has executed sucessfully
        """
        test_passed = True
        if self.expectTry("", "login", 90):
            print "##Sucessfully reached log in prompt##"
        else:
            print "##Failed to reach Linux login => no tests will be ran on this device##\n"
            test_passed = False
        return test_passed


    def login(self):
        """
        Log into Linux as root
        """
        test_passed = True
        if self.expectTry("root", "#", 5):
            print "##Logged into Linux##"
        else:
            print "##Failed to login => no tests will be ran on this device##\n"
            test_passed = False

        # NOTE: this may be temporary solution
        # Grab the command line prompt if it exists
        #self.proc.logfile_read.seek(0)
        #promptString = self.proc.logfile_read.readlines()[-1]
        #self.promptString = promptString if "@" in promptString else ''
        return test_passed


    def execute(self, cmd, response, timeOut=5):
        """
        Wrapper used to execute each test suite
        """
        if self.expectTry(cmd, response, timeOut):
            print "##Successfully executed '%s'##" % cmd
            return self.proc.before + self.proc.after, True
        else:
            print "##Failed to execute '%s'##" % cmd
            return self.proc.before, False
