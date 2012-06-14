def run(self, test, resultDir):
    lst = []
    testDict = dict(test)
    for item in testDict:
        #if the test is a special test, run it
        if item in dir(Tests):
            method = getattr(self, item)
            out = method(testDict[item])
        #else run the generic test
        else:
            cmd = self.get_cmd(item)
            out = self.generic_test(item, cmd, testDict[item])
        lst.append(out)

    output = open(os.path.join(resultDir,'results'),'wb')
    #using pickle to maintain the dict datatype when writing it to file
    pickle.dump(lst, output)
    output.close()

def get_cmd(self, test):
    #this dict holds the commands to be run for all the generic tests
    cmdDict = {
    'cpu_type': 'cat /proc/cpuinfo',
    'ethernet_exists': 'ifconfig',
    'ethernet_irq': 'dmesg',
    'ethernet_iperf': 'iperf -c factory.gumstix.net',
    "usb_console_detected": 'lsusb'
    }
    return cmdDict[test]

#TODO: pass in regex for expect instead of string
def generic_test(self, testName, cmd, expect):
    localResult ={
    'measurement':{}, #measurement field on dash
    'message':{},
    'result':{}, #pass/fail/skip
    'test_case_id':{}
    }

    startTime = time.time()
    rawOut = self.conn.execute(cmd)
    timeDiff = time.time()-startTime
    cleanOut = ''
    for line in rawOut.split('\n'):
        if is_ascii(line):
            cleanOut = cleanOut + line
        else:
            cleanOut = cleanOut + "##Non-Ascii characters were detected here##\n"

    #TODO: add a 'skipped' state
    if expect in cleanOut:
        localResult['result'] = 'pass'
    else:
        localResult['result'] = 'fail'

    localResult['message'] = cleanOut
    localResult['measurement'] = timeDiff
    localResult['test_case_id'] = testName
    return localResult
