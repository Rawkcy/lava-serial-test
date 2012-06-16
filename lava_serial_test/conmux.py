# Mustafa Faraj (mustafa@gumstix.com)
# Roxanne Guo (roxanne@gumstix.com

import tempfile
import pexpect
import os
import re


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
        self.promptString = 'testing@gumstix\([0-9]+\)#'
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

        self.setPromptString()
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


    def setPromptString(self):
        """
        Manually setting system's PS1
        """
        self.proc.sendline("export PS1='testing@gumstix(`echo -n $?`)# '")
        # Just to flush out self.proc.before and after
        self.proc.expect('#', timeout=5)


    #FIXME
    def do(self, cmd, timeout=5):
        """
        Returns pexpect's response
        """
        import ipdb;ipdb.set_trace()
        self.proc.sendline(cmd)
        try:
            self.proc.expect(self.promptString, timeout=timeout)
        except pexpect.TIMEOUT:
            print 'Command %s TIMED OUT' % cmd
            return (-1, 'pexpect timed out while executing %s ' % cmd)

        info = self.proc.before.split('\n')
        cmdprompt = info.pop()
        return_code = int(re.search('(?P<code>[0-9]+)', cmdprompt).group())
        return (return_code, info)
