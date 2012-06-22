# Mustafa Faraj (mustafa@gumstix.com)
# Roxanne Guo (roxanne@gumstix.com

import tempfile
import pexpect
import os
import re


# TODO: conmux connection sometimes requires reset
class ConmuxConnection(object):

    def __init__(self, board, result_dir):
        """
        Creates a conmux connection instance for testing over serial
        Holds all methods in association with the serial connection
        """
        self.board = board
        self.promptRegex = 'testing@gumstix\([0-9]+\)'

        # If ran standalone, save log and json to specified folder
        # Otherwise, default to /tmp/*_logs
        if result_dir == os.getcwd():
            self.logDirectory = os.getcwd()
        else:
            self.logDirectory = result_dir + '_logs'
            if not os.path.exists(self.logDirectory):
                os.makedirs(self.logDirectory)
        logfile = file(os.path.join(self.logDirectory, '%s.log' % self.board), 'w+r')
        self.proc = pexpect.spawn("conmux-console %s" % self.board, timeout=240)
        self.proc.logfile_read = logfile
        self.proc.setecho(False)


    def expectTry(self, cmdToSend, stringToExpect, timeOut):
        """
        Modular function used to singularly execute a command and
        expect an output

        Returns whether or not the pexpect matched a result
        """
        cmd_passed = True
        if cmdToSend:
            self.proc.sendline(cmdToSend)
        try:
            self.proc.expect(stringToExpect, timeout=timeOut)
        except pexpect.TIMEOUT:
            # Clear command line with `Ctrl-C and CF`
            print "Command '%s' timed out" % cmdToSend
            print "Failed to match with '%s'" % stringToExpect
            self.proc.sendintr()
            self.proc.sendline()
            cmd_passed = False
        return cmd_passed


    def setPromptString(self):
        """
        Manually setting system's PS1

        Used to extract return code of shell commands
        """
        self.proc.sendline("export PS1='testing@gumstix(`echo -n $?`)# '")
        # Just to flush out self.proc.before and after
        self.proc.expect('#', timeout=5)


    def uBoot(self):
        """
        First "test suite" to be executed
        Begins the log file by logging the uBoot sequence
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

        Returns the entire execution output as seen by pexpect
        """
        if self.expectTry(cmd, response, timeOut):
            print "##Successfully executed '%s'##" % cmd
            return self.proc.before + self.proc.after, True
        else:
            print "##Failed to execute '%s'##" % cmd
            return self.proc.before, False


    def get_shellcmdoutput(self, cmd, timeout=5):
        """
        Executes shell command

        Returns the return code as integer and list of stdout
        """
        self.proc.sendline(cmd)
        reg_match = '#.*' + self.promptRegex
        try:
            # Clear the first command match
            self.proc.expect(reg_match, timeout=timeout)
        except pexpect.TIMEOUT:
            print 'Command %s TIMED OUT' % cmd
            return (-1, 'pexpect timed out while executing %s ' % cmd)

        info = self.proc.after.split('\n')[1:]
        cmdprompt = info.pop()
        return_code = int(re.search('(?P<code>[0-9]+)', cmdprompt).group())
        return (return_code, info)
