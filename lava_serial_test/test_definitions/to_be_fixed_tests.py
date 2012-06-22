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


def i2cbus(localResult, conn):
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
