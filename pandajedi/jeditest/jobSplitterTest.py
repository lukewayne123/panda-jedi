# logger
from pandacommon.pandalogger.PandaLogger import PandaLogger
logger = PandaLogger().getLogger('JobGenerator')
from pandajedi.jedicore.MsgWrapper import MsgWrapper
tmpLog = MsgWrapper(logger)

from pandajedi.jedicore.JediTaskBufferInterface import JediTaskBufferInterface

tbIF = JediTaskBufferInterface()
tbIF.setupInterface()

siteMapper = tbIF.getSiteMapper()

from pandajedi.jediddm.DDMInterface import DDMInterface

ddmIF = DDMInterface()
ddmIF.setupInterface()

from pandajedi.jediorder.JobBroker import JobBroker
from pandajedi.jediorder.JobSplitter import JobSplitter
from pandajedi.jediorder.JobGenerator import JobGeneratorThread
from pandajedi.jedicore.ThreadUtils import ThreadPool
from pandajedi.jediorder.TaskSetupper import TaskSetupper

import sys
jediTaskID = int(sys.argv[1])
try:
    datasetID = [int(sys.argv[2])]
except:
    datasetID = None

s,taskSpec = tbIF.getTaskWithID_JEDI(jediTaskID)

cloudName = taskSpec.cloud
vo = taskSpec.vo
prodSourceLabel = taskSpec.prodSourceLabel 
queueID = taskSpec.workQueue_ID

workQueue = tbIF.getWorkQueueMap().getQueueWithID(queueID)

threadPool = ThreadPool()

# get typical number of files
typicalNumFilesMap = tbIF.getTypicalNumInput_JEDI(vo,prodSourceLabel,workQueue,
                                                  useResultCache=600)

tmpListList = tbIF.getTasksToBeProcessed_JEDI(None,vo,workQueue,
                                              prodSourceLabel,
                                              cloudName,nFiles=10,simTasks=[jediTaskID],
                                              fullSimulation=True,
                                              typicalNumFilesMap=typicalNumFilesMap,
                                              simDatasets=datasetID)

taskSetupper = TaskSetupper(vo,prodSourceLabel)
taskSetupper.initializeMods(tbIF,ddmIF)

for dummyID,tmpList in tmpListList:
    for taskSpec,cloudName,inputChunk in tmpList:
        jobBroker = JobBroker(taskSpec.vo,taskSpec.prodSourceLabel)
        tmpStat = jobBroker.initializeMods(ddmIF.getInterface(vo),tbIF)
        splitter = JobSplitter()
        gen = JobGeneratorThread(None,threadPool,tbIF,ddmIF,siteMapper,False,taskSetupper,None)

        taskParamMap = None
        if taskSpec.useLimitedSites():
            tmpStat,taskParamMap = gen.readTaskParams(taskSpec,taskParamMap,tmpLog)

        tmpStat,inputChunk = jobBroker.doBrokerage(taskSpec,cloudName,inputChunk,taskParamMap)

        tmpStat,subChunks = splitter.doSplit(taskSpec,inputChunk,siteMapper)

        tmpStat,pandaJobs,datasetToRegister,oldPandaIDs = gen.doGenerate(taskSpec,cloudName,subChunks,inputChunk,tmpLog,True)
        if taskSpec.useEventService():
            pandaJobs = gen.increaseEventServiceConsumers(pandaJobs,taskSpec.getNumEventServiceConsumer())

