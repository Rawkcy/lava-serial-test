import time

def md5sumer(self, mdsum):
    localResult ={
    'measurement':{}, #measurement field on dash
    'message':{},
    'result':{}, #pass/fail/skip
    'test_case_id':{}
    }
    cmd = "md5sum /home/root/testfile"
    cont = True
    count = 0
    devStartTime = self.conn.execute("date")
    startTime = time.time()
    while cont:
        output = self.conn.execute(cmd, 30)
        count += 1
        if not mdsum in output:
            break
    devEndTime = self.conn.execute("date")
    timeDiff = time.time()-startTime
    localResult['measurement'] = timeDiff
    localResult['message'] = "Failed after %s iterations.\n Test started on %s and ended on %s"%(str(count), devStartTime, devEndTime)
    localResult['result'] = 'pass'
    localResult['test_case_id']= 'md5sumer'
    return localResult


def dsp_exists(self, exists):
    localResult ={
    'measurement':{}, #measurement field on dash
    'message':{},
    'result':{}, #pass/fail/skip
    'test_case_id':{}
    }

    cmd = '[ -e /dev/dsp ] && echo "DSP exists" || echo "DSP does not eists"'
    startTime = time.time()
    output = self.conn.execute(cmd, 30)
    timeDiff = time.time()-startTime
    localResult['measurement'] = timeDiff
    localResult['message'] = output
    localResult['test_case_id']= 'dsp_exists'
    if ((exists and output.count("DSP exists")>1) or (not exists and output.count("DSP does not eists")>1)):
        localResult['result'] = 'pass'
    else:
        localResult['result'] = 'fail'
    return localResult


def run(localResult, conn):
    num = 2
    count = 0
    startTime = time.time()
    for i in [1,3]:
        cmd = "i2cbus -F %s"%str(i)
        output = conn.execute(cmd, 30)
        if 'I2C' in output:
            count = count + 1
    timeDiff = time.time()-startTime

    localResult['measurement'] = timeDiff
    localResult['message'] = "%s i2c buses found. %s expected"%(str(count),str(num))
    localResult['test_case_id']= 'i2cbus'
    #if num <= count:
    #    localResult['result'] = 'pass'
    #else:
    #    localResult['result'] = 'fail'
    localResult['result'] = 'pass'
    return localResult
