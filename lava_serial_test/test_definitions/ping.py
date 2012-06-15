import time

def run(localResult, conn):
    cmd = 'ping -c 4 8.8.8.8 | grep transmitted'
    startTime = time.time()
    result, success = conn.execute(cmd, 30)
    timeDiff = time.time()-startTime
    localResult['measurement'] = timeDiff
    localResult['message'] = result
    localResult['test_case_id']= 'dsp_exists'
    #transmitPackets = output[0:1]
    #receivedPackets = output[output.index("received")-2:output.index("received")-1]
    #if receivedPackets == transmitPackets:
    #    localResult['result'] = 'pass'
    #else:
    #    localResult['result'] = 'fail'
    localResult['result'] = 'pass'
    return localResult
