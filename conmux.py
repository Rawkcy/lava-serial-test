# Author: Mustafa Faraj (vis.mustafa@gmail.com)
#
# This file is part of the Gumstix modification for the LAVA Dispatcher.
# This file contains all the tests that can run on any Gumstix Overo device.

import pexpect
import os

class ConmuxConnection():
    #Small change to commit to git
    def __init__(self, profile, resultsDir):
        self.profile = profile
        self.promptString = ''
        self.resultsDir = resultsDir
        self.proc = pexpect.spawn("conmux-console " + self.profile, timeout=240)
        conDir = os.path.join(resultsDir,"conmux")
        if not os.path.exists(conDir):
            os.system('mkdir -p %s' % conDir)
        self.logFile = file(os.path.join(conDir, "CCTemp.txt"), 'w')
        self.proc.logfile = self.logFile
        self.proc.setecho(False)

    #TODO: Add a function to reset the conmux connection
    #this is a helper function that sends cmdToSend to the
    #board and expects StringToExpect within timeOut seconds.
    #If it gets what's expected, it returns 0, otherwise -1
    def expectTry(self, cmdToSend, stringToExpect, timeOut):
        if len(cmdToSend) > 0:
            self.proc.sendline(cmdToSend)
        try:
            self.proc.expect(stringToExpect, timeout=timeOut)
        except:
            #TODO: remove the next 3 lines. They are debug lines
            print "didnt find %s" %stringToExpect
            print (self.proc.before, self.proc.after)
            raw_input("stopping here")
            return -1
        return 0

    def logBootup(self):
        ret = 0
        #Put the log in a directory, so that lava doesnt think its a result file
        bootLogDir = os.path.join(self.resultsDir, 'bootlog')
        if not os.path.exists(bootLogDir):
            os.mkdir(bootLogDir)
        f = file(os.path.join(bootLogDir,"log.txt"), 'w+')
        #send an enter, and expect "Starting kernel withing 45 seconds"
        if self.expectTry(" ", "Starting kernel", 45):
            print "##Failed in uBoot"
            f.write("Failed in uBoot. No Tests will be run on this device.")
            ret = -1
        else:
            print "##Got past uBoot##"

        try:
            uBootLog =  self.proc.before + self.proc.after
        except:
            uBootLog = self.proc.before
        f.write(uBootLog)

        #TODO: make the "login" a controllable parameter
        if self.expectTry("", "login", 90):
            print "##Failed to boot Linux up##"
            f.write("Failed in booting up Linux. No Tests will be run on this device.")
            ret = -1
        else:
            print "##Booted into Linux##"

        try:
            linuxLog =  self.proc.before + self.proc.after
        except:
            linuxLog = self.proc.before
        f.write(linuxLog)
        f.close()
        return ret


    def login(self):
        rc = -1
        if self.expectTry("root", "#", 5):
            print "##Failed to log into Linux##"
            return rc
        else:
            print "##Logged into Linux##"
        log = open(os.path.join(self.resultsDir, "conmux", "CCTemp.txt"), 'r')
        for line in log.readlines():
            if "@" in line:
                PS = line
                rc = 0

        log.close()
        self.promptString = PS
        return rc

    def execute(self, cmd, timeOut=30):
        rc = -1
        #empty the pexpect log file
        self.proc.logfile.close()
        self.logFile.close()
        self.logFile = file(os.path.join(self.resultsDir, "conmux", "CCTemp.txt"), 'w')
        self.proc.logfile = self.logFile
        #Execute the command
        if self.expectTry(cmd, self.promptString, timeOut):
            print "##Failed to execute \"%s\"##" %cmd
            rc = -1
            rmsg = "Failed to execute \"%s\"" %cmd
        else:
            print "##Executed \"%s\" successfully##" %cmd
        #get the command output
        resultsFile = open(os.path.join(self.resultsDir, "conmux", "CCTemp.txt"), 'r')
        results = resultsFile.read()
        resultsFile.close()
        bootLogDir = os.path.join(self.resultsDir, 'bootlog')
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
