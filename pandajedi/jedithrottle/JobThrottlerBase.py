from pandajedi.jedicore import Interaction

# throttle level
THR_LEVEL5 = 5

# base class for job throttle
class JobThrottlerBase (object):

    def __init__(self,taskBufferIF):
        self.taskBufferIF = taskBufferIF
        # returns
        self.retTmpError    = self.SC_FAILED,True
        self.retThrottled   = self.SC_SUCCEEDED,True
        self.retUnThrottled = self.SC_SUCCEEDED,False
        self.retMergeUnThr  = self.SC_SUCCEEDED,THR_LEVEL5
        # limit
        self.maxNumJobs  = None
        self.minPriority = None
        self.refresh()
        self.msgType      = 'jobthrottler'


    # refresh
    def refresh(self):
        self.siteMapper = self.taskBufferIF.getSiteMapper()

        
    # set maximum number of jobs to be submitted    
    def setMaxNumJobs(self,maxNumJobs):
        self.maxNumJobs = maxNumJobs


    # set min priority of jobs to be submitted
    def setMinPriority(self,minPriority):
        self.minPriority = minPriority


    # check throttle level
    def mergeThrottled(self,thrLevel):
        # un-leveled flag
        if thrLevel in [True,False]:
            return thrLevel
        return thrLevel > THR_LEVEL5
        


Interaction.installSC(JobThrottlerBase)
