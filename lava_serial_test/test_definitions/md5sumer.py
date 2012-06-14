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
