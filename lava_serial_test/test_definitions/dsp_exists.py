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
