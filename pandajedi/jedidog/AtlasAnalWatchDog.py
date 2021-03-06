import re
import sys

from pandajedi.jedicore.MsgWrapper import MsgWrapper
from WatchDogBase import WatchDogBase
from pandaserver.dataservice.Activator import Activator

# logger
from pandacommon.pandalogger.PandaLogger import PandaLogger
logger = PandaLogger().getLogger(__name__.split('.')[-1])



# watchdog for ATLAS analysis
class AtlasAnalWatchDog (WatchDogBase):

    # constructor
    def __init__(self,ddmIF,taskBufferIF):
        WatchDogBase.__init__(self,ddmIF,taskBufferIF)



    # main
    def doAction(self):
        try:
            # get logger
            tmpLog = MsgWrapper(logger)
            tmpLog.debug('start')
            origTmpLog = tmpLog
            # check every 60 min
            checkInterval = 60
            # get lib.tgz for waiting jobs
            libList = self.taskBufferIF.getLibForWaitingRunJob_JEDI(self.vo,self.prodSourceLabel,checkInterval)
            tmpLog.debug('got {0} lib.tgz files'.format(len(libList)))
            # activate or kill orphan jobs which were submitted to use lib.tgz when the lib.tgz was being produced
            for prodUserName,datasetName,tmpFileSpec in libList:
                tmpLog = MsgWrapper(logger,'<jediTaskID={0}>'.format(tmpFileSpec.jediTaskID))
                tmpLog.debug('start')
                # check status of lib.tgz
                if tmpFileSpec.status == 'failed':
                    # get buildJob 
                    pandaJobSpecs = self.taskBufferIF.peekJobs([tmpFileSpec.PandaID],
                                                               fromDefined=False,
                                                               fromActive=False,
                                                               fromWaiting=False)
                    pandaJobSpec = pandaJobSpecs[0]
                    if pandaJobSpec != None:
                        # kill
                        self.taskBufferIF.updateJobs([pandaJobSpec],False)
                        tmpLog.debug('  killed downstream jobs for user="{0}" with libDS={1}'.format(prodUserName,datasetName))
                    else:
                        # PandaJobSpec not found
                        tmpLog.error('  cannot find PandaJobSpec for user="{0}" with PandaID={1}'.format(prodUserName,
                                                                                                         tmpFileSpec.PandaID))
                elif tmpFileSpec.status == 'finished':
                    # set metadata
                    self.taskBufferIF.setGUIDs([{'guid':tmpFileSpec.GUID,
                                                 'lfn':tmpFileSpec.lfn,
                                                 'checksum':tmpFileSpec.checksum,
                                                 'fsize':tmpFileSpec.fsize,
                                                 'scope':tmpFileSpec.scope,
                                                 }])
                    # get lib dataset
                    dataset = self.taskBufferIF.queryDatasetWithMap({'name':datasetName})
                    if dataset != None:
                        # activate jobs
                        aThr = Activator(self.taskBufferIF,dataset)
                        aThr.start()
                        aThr.join()
                        tmpLog.debug('  activated downstream jobs for user="{0}" with libDS={1}'.format(prodUserName,datasetName))
                    else:
                        # datasetSpec not found
                        tmpLog.error('  cannot find datasetSpec for user="{0}" with libDS={1}'.format(prodUserName,datasetName))
                else:
                    # lib.tgz is not ready
                    tmpLog.debug('  keep waiting for user="{0}" libDS={1}'.format(prodUserName,datasetName))
        except:
            tmpLog = origTmpLog
            errtype,errvalue = sys.exc_info()[:2]
            tmpLog.error('failed with {0} {1}'.format(errtype,errvalue))
        # return
        tmpLog = origTmpLog
        tmpLog.debug('done')
        return self.SC_SUCCEEDED
    
