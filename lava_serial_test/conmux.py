# Mustafa Faraj (vis.mustafa@gmail.com)
# Roxanne Guo (roxane.guo@gmail.com)

import tempfile
import pexpect
import os

# TODO: conmux connection sometimes requires reset
class ConmuxConnection():

    def __init__(self, board):
        """
        Creates a conmux connection instance for testing over serial
        """
        self.board = board
        self.promptString = ''
        self.logDirectory = tempfile.mkdtemp(suffix='_logs')
        if not os.path.exists(self.logDirectory):
            os.makedirs(self.logDirectory)
        logFile = file(os.path.join(self.logDirectory, "%s.log", % self.board), 'w+')
        self.proc = pexpect.spawn("conmux-console %s" % self.board, logfile=logfile, timeout=240)
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
            print "Command '%s' was not successful" % cmdToSend
            print "Failed to match with '%s'" % stringToExpect
            raw_input("Press <enter> to continue")
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
            print "##Failed to execute uBoot => no tests will be ran on this device\n##"
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
            print "##Failed to execute uBoot => no tests will be ran on this device\n##"
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
            print "##Failed to execute uBoot => no tests will be ran on this device\n##"
            test_passed = False

        # NOTE: this may be temporary solution
        # Grab the command line prompt if it exists
        promptString = open(self.proc.logFile, 'r').readlines()[-1]
        self.promptString = promptString if "@" in promptString else ''
        return test_passed


    def execute(self, cmd, timeOut=30):
        """
        Wrapper used to execute each test suite
        """
        # Execute the test
        if self.expectTry(cmd, self.promptString, timeOut):
            print "##Successfully executed '%s'##" % cmd
            return self.proc.before + self.proc.after, True
        else:
            print "##Failed to execute '%s'##" % cmd
            return self.proc.before, False
