from userinterface import Client

import sys
site = sys.argv[1]
import uuid

dsName = 'mc12_8TeV.189659.gg2VVPythia8_AU2CT10_ggH125p5_VV_2mu2numu_m2l4_2pt3.evgen.EVNT.e2872_tid01461041_00'
logDatasetName = 'panda.jeditest.log.{0}'.format(uuid.uuid4())

taskParamMap = {}

#taskParamMap['nFilesPerJob'] = 1
taskParamMap['nFiles'] = 1
taskParamMap['nEventsPerFile']   = 5000
taskParamMap['nEventsPerWorker'] = 10 #5000
taskParamMap['nEventsPerJob'] = 1000
taskParamMap['nEvents'] = 1000
#taskParamMap['skipScout'] = True
taskParamMap['objectStore'] = 'root^atlas-objectstore.cern.ch^/atlas/eventservice'
taskParamMap['taskName'] = str(uuid.uuid4())
taskParamMap['userName'] = 'pandasrv1'
taskParamMap['vo'] = 'atlas'
taskParamMap['taskPriority'] = 900
#taskParamMap['reqID'] = reqIdx
taskParamMap['architecture'] = 'x86_64-slc5-gcc43-opt'
taskParamMap['transUses'] = 'Atlas-17.2.11'
taskParamMap['transHome'] = 'AtlasProduction-17.2.11.8'
taskParamMap['transPath'] = 'AtlasG4_tf.py'
taskParamMap['processingType'] = 'simul'
taskParamMap['prodSourceLabel'] = 'ptest'
taskParamMap['taskType'] = 'prod'
taskParamMap['workingGroup'] = 'AP_Higgs'
taskParamMap['coreCount'] = 1
taskParamMap['walltime'] = 1
taskParamMap['cloud'] = 'US'
taskParamMap['site'] = site
taskParamMap['log'] = {'dataset': logDatasetName,
                       'type':'template',
                       'param_type':'log',
                       'token':'ATLASDATADISK',
                       'offset':1000,
                       'value':'{0}.${{SN}}.log.tgz'.format(logDatasetName)}
outDatasetName = 'panda.jeditest.HITS.{0}'.format(uuid.uuid4())


taskParamMap['jobParameters'] = [
    {'type':'constant',
     'value': '--AMITag s1831 --DBRelease=current --athenaopts=--preloadlib=${ATLASMKLLIBDIR_PRELOAD}/libimf.so --conditionsTag=OFLCOND-MC12-SIM-00',
     },
    {'type':'template',    
     'value':'firstEvent=${FIRSTEVENT}',
     'param_type':'number',
     },
    {'type':'constant',
     'value': '--geometryVersion=ATLAS-GEO-21-02-02_VALIDATION',
     },
    {'type':'template',
     'param_type':'input',
     'value':'--inputEvgenFile=${IN}',
     'dataset':dsName,
     },
    {'type':'template',    
     'value':'--maxEvents=${MAXEVENTS}',
     'param_type':'number',
     },
    {'type':'template',
     'param_type':'output',
     'token':'ATLASDATADISK',     
     'value':' --outputHitsFile={0}.${{SN}}.pool.root'.format(outDatasetName),
     'dataset':outDatasetName,
     },
    {'type':'constant',    
     'value':'--physicsList=QGSP_BERT --postInclude=RecJobTransforms/UseFrontierFallbackDBRelease.py --preInclude=SimulationJobOptions/preInclude.FrozenShowersFCalOnly.py,SimulationJobOptions/preInclude.BeamPipeKill.py',
     },
    {'type':'template',    
     'value':'--skipEvents=${SKIPEVENTS}',
     'param_type':'number',
     },
    {'type':'template',    
     'value':'--randomSeed=${RNDMSEED}',
     'param_type':'number',
     },
    ]

taskParamMap['esmergeSpec'] = {}
taskParamMap['esmergeSpec']['transPath'] = 'Merge_trf.py'
taskParamMap['esmergeSpec']['jobParameters'] = "aaa bbb"

print Client.insertTaskParams(taskParamMap)