# Mustafa Faraj (vis.mustafa@gmail.com)
# Roxanne Guo (roxane.guo@gmail.com)

import pexpect
import os

# TODO: conmux connection sometimes requires reset
class ConmuxConnection():

    def __init__(self, board):
        """
        Creates a conmux connection instance for the serial test
        """
        self.board = board
        self.promptString = ''
        self.logDirectory = '/tmp/lava-serial-test-logs/'
        self.proc = pexpect.spawn("conmux-console " + self.board, timeout=240)

        # TODO: fix log file creation ..
        self.logFile = file(os.path.join(self.logDirectory, "%s.log", % self.board), 'w+')
        self.proc.logfile = self.logFile
        self.proc.setecho(False)
        self.logFile.close()

    def expectTry(self, cmdToSend, stringToExpect, timeOut):
        """
        Modular function used to specifically execute a command and
        expect an output
        """
        cmd_passed = True
        if len(cmdToSend) > 0:
            self.proc.sendline(cmdToSend)
        try:
            self.proc.expect(stringToExpect, timeout=timeOut)
        except:
            print "Command '%s' was not successful" % cmdToSend
            print "Failed to match with '%s'" % stringToExpect
            raw_input("Press <enter> to continue")
            cmd_passed = False
        return cmd_passed


    def uBoot(self):
        """
        First "test suite" to be executed
        Begins the log file by executing uboot
        """
        test_passed = True
        # Send an enter press and expect the string "Starting kernel withing 45 seconds"
        if self.expectTry(" ", "Starting kernel", 45):
            print "##uBoot was executed##"
        else:
            print "##Failed to execute uBoot##"
            f.write("Failed to execute uBoot. No tests will be ran on this device.")
            test_passed = False

        # Write to log file
        try:
            uBootLog =  self.proc.before + self.proc.after
        except:
            uBootLog = self.proc.before
        f = open(self.logFile, 'w+')
        f.write(uBootLog)
        f.close()
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
            print "##Failed to boot Linux up##"
            f.write("Failed to boot up Linux. No tests will be ran on this device.")
            test_passed = False

        # Write to log file
        try:
            loginPromptLog =  self.proc.before + self.proc.after
        except:
            loginPromptLog = self.proc.before
        f = open(self.logFile, 'w+')
        f.write(loginPromptLog)
        f.close()
        return test_passed


    def login(self):
        """
        Log into Linux as root
        """
        test_passed = True
        if self.expectTry("root", "#", 5):
            print "##Logged into Linux##"
        else:
            print "##Failed to log into Linux##"
            test_passed = False

        # FIXME
        log = open(self.logFile, 'r')
        for line in log.readlines():
            if "@" in line:
                PS = line
                #break? Why do we need to run in for loop once we have found it?
        log.close()
        self.promptString = PS
        return test_passed

    # FIXME
    def execute(self, cmd, timeOut=30):
        rc = -1
        #empty the pexpect log file
        self.proc.logfile.close()
        self.logFile.close()
        self.logFile = file(os.path.join(self.logDirectory, "conmux", "CCTemp.txt"), 'w')
        self.proc.logfile = self.logFile
        #Execute the command
        if self.expectTry(cmd, self.promptString, timeOut):
            print "##Failed to execute \"%s\"##" %cmd
            rc = -1
            rmsg = "Failed to execute \"%s\"" %cmd
        else:
            print "##Executed \"%s\" successfully##" %cmd
        #get the command output
        resultsFile = open(os.path.join(self.logDirectory, "conmux", "CCTemp.txt"), 'r')
        results = resultsFile.read()
        resultsFile.close()
        bootLogDir = os.path.join(self.logDirectory, 'bootlog')
        if os.path.exists(os.path.join(bootLogDir, "log.txt")):
            bootlog = file(os.path.join(bootLogDir,"log.txt"), 'a')
            bootlog.write(results)
            bootlog.flush()
            bootlog.close()
        try:
            #if execution failed, return rmsg
            return rmsg
        except:
            #else return the result
            return results
