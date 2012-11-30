import os
import sys
import time
import commands
import string
import logging
import datetime 
from exceptions import *
import sets

class commonconf:

   def __init__(self):
        #INITIALIZATION GLOBAL CONFIGURATION
        self.PRODUCTS  = { # 'PRODUCT NAME' : ['TAG1', 'TAG2'],
                                      'LFC' : ['INTEGRATION','UI'], 
                                      'DPM' : ['INTEGRATION'],
                                   'DCACHE' : ['INTEGRATION'],
                                    'CREAM' : ['INTEGRATION', 'UI', 'MPI', 'WNODES'],
                                      'WMS' : ['INTEGRATION', 'UI'],
                                 'LCGUTILS' : ['INTEGRATION'],
                                    'STORM' : ['INTEGRATION']
                         }
        self.CONFFILES = {      'CEoutfile' : './OUT/CEoutfile.txt',
                                'MPIJDL'    : './JDL/mpitest.jdl',
                                'BASICJDL'  : './JDL/basictest.jdl',
                             'CEMPIoutfile' : './OUT/CEMPIoutfile.txt',
                               'WMSoutfile' : './OUT/WMSoutfile.txt',
                               'SOURCEFILE' : './JDL/basictest.jdl'
                           }
        self.TESTBED =   {           'CREAMCE' : {'RESOURCES':  ['emitestbed02.cnaf.infn.it:8443/cream-sge-emitesters',
                                                                'emitestbed09.cnaf.infn.it:8443/cream-sge-emitesters',
                                                                'emi-demo08.cnaf.infn.it:8443/cream-lsf-testers',
                                                                'emi-demo13.cnaf.infn.it:8443/cream-pbs-demo',
                                                                'emitestbed32.cnaf.infn.it:8443/cream-lsf-testers',
                                                                'emitestbed29.cnaf.infn.it:8443/cream-pbs-demo'] 
                                     },
                           
                     'CREAMCE_MPI': {'RESOURCES': ['emitestbed29.cnaf.infn.it:8443/cream-pbs-demo',
                                                   'cert-07.cnaf.infn.it:8443/cream-pbs-demo']
                                    },
                           
                           'STORM': {'RESOURCES': ['emitestbed03.cnaf.infn.it', 'emitestbed25.cnaf.infn.it'],
                                         'VODIR': ['testers.eu-emi.eu', 'testers.eu-emi.eu'],
                                      'DESTPATH': ['destpathtest/file1', 'destpathtest/file1'],
                                   'DESTGUCPATH': ['/tmp/file1', '/tmp/file1']
                                     },
                           
                           'WMS' :  {'RESOURCES': ['https://cert-08.cnaf.infn.it:7443/glite_wms_wmproxy_server',
                                                   'https://cert-13.cnaf.infn.it:7443/glite_wms_wmproxy_server',
                                                   'https://cert-27.cnaf.infn.it:7443/glite_wms_wmproxy_server']
                                     },
                           
                        'WNODES' : {'RESOURCES':  ['emi-demo13.cnaf.infn.it:8443/cream-pbs-qwnodes',
                                                   'emi-demo13.cnaf.infn.it:8443/cream-pbs-qwnodessl6']
                                    },
                           
                          'VOMS' : {     'VO': 'testers.eu-emi.eu',
				    'RESOURCES': 'emitestbed07.cnaf.infn.it' },
                      'BDII_TOP' : {'RESOURCES': 'certtb-bdii-top.cern.ch:2170'},
                      'BDII_SITE': {'RESOURCES': 'certtb-bdii-site.cern.ch:2170',
                                    'SITE_NAME': 'cert-tb-cern'
                                   },
                                    
                        'DCACHE' : {'RESOURCES': ['cork.desy.de'],
                                       'VODIR' : ['/pnfs/desy.de/data/testers.eu-emi.eu'],
                                     'DESTPATH': ['destpathtest', 'destpathtest'],
                                   },
                                   
                           'LFC' : {'RESOURCES': ['emi2rc-sl5-lfc.cern.ch:/grid/testers.eu-emi.eu/'],
                                     'TESTDIR': ['destpathtest']
                                   },
                        
                           'DPM' : {'RESOURCES': ['lxbra1910.cern.ch']
                                   }
                          }
        self.UTILS_CLI  = {       'CREAM'  :  {                   'SUBMIT' : 'glite-ce-job-submit -n  -r ENDPOINT -a JDL',
                                                               'JOBSTATUS' : 'glite-ce-job-status JOBID',
                                                            'SERVICEINFO'  : 'glite-ce-service-info ENDPOINT'
                                              },
                                     'WMS' :  {                   'SUBMIT' : 'glite-wms-job-submit --nomsg  -e ENDPOINT -a JDL',
                                                               'JOBSTATUS' : 'glite-wms-job-status JOBID',
                                                                  'CHECK'  :  'uberftp ENDPOINT ls |grep -c logged'
                                              },
                                     'SRM' :  {                     'PING' : 'clientSRM ping -e httpg://ENDPOINT:8444',
                                                                  'MKDIR'  : 'srmmkdir -2 -debug srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                                      'RM' : 'srmrm  srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                                   'RMDIR' : 'srmrmdir  srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH', 
                                                                      'LS' : 'srmls -2 srm://ENDPOINT:8443/VODIR/',
                                                                      'CP' : 'srmcp -2 srm://ENDPOINT:8443/VODIR/DESTFILE file:///`pwd`/TESTFILE'
                                              },
                                  'GLOBUS' :  {                      'GUC' : 'globus-url-copy file://`pwd`/TESTFILE   gsiftp://ENDPOINT:2811/DESTPATH' 
                                              },
                                    'LDAP' :  {           'SEARCHRESOURCE' : 'ldapsearch -x -H ldap://ENDPOINT:2170/ -b mds-vo-name=resource,o=grid',
                                                           'SEARCHTOPBDII' : 'ldapsearch -x -H  ldap://BDII_TOP -b mds-vo-name=local,o=grid',
                                                          'SEARCHSITEBDII' : 'ldapsearch -x -H  ldap://BDII_SITE -b mds-vo-name=SITE_NAME,o=grid' ,
                                                         'SEARCH_SITE_OBJ' : "ldapsearch -x -H  ldap://BDII_SITE -b mds-vo-name=SITE_NAME,o=grid 'objectclass: GlueTop' "
                                              },
                                'LCGUTILS' :  {                       'LS_SRM' : 'lcg-ls -v -l -b -D srmv2 srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                                      'CP_SRM' : 'lcg-cp -b --verbose -D srmv2 file://`pwd`/TESTFILE srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                                         'LS' : 'lcg-ls --verbose ENDPOINT',
                                                                     'CR_LFN' : 'lcg-cr -l lfn:/grid/VOMS/DESTFILE  -d ENDPOINT file:///`pwd`/TESTFILE',
                                                                     'LR_LFN' : 'lcg-lr lfn:/grid/VOMS/TESTFILE',
                                                                    'DEL_LFN' : 'lcg-del -a lfn:/grid/VOMS/TESTFILE',
                                                                  'INFOSITES' : 'lcg-infosites --vo VOMS all',
                                                               'INFOSITES_CE' : 'lcg-infosites --vo VOMS ce',
                                                               'INFOSITES_SE' : 'lcg-infosites --vo VOMS se',
                                                          'INFOSITES_BDIITOP' : 'lcg-infosites --vo VOMS bdii_top',
                                                         'INFOSITES_BDIISITE' : 'lcg-infosites --vo VOMS bdii_site',
                                                                  'INFO_CE'   : 'lcg-info --list-ce --vo VOMS',
                                                                  'INFO_SE'   : 'lcg-info --list-se --vo VOMS',
                                                        'INFO_SE_ATTR_NAME'   : 'lcg-info --list-se --attrs SEName',
                                                },

                                   'VOMS'  :   {               'PROXYINFO' : 'voms-proxy-info -all',
                                                               'PROXYCHECK': 'voms-proxy-info -vo -exists -hours 6'
                                                }, 
                                   'LFC'   :   {                      'LS' : 'lfc-ls -l ENDPOINT',
                                                                   'MKDIR' : 'lfc-mkdir ENDPOINT/TESTDIR',
                                                                   'RMDIR' : 'lfc-rm -r ENDPOINT/TESTDIR'
                                               },
                          }
              
        self.ID=''
        self.NUM_STATUS_RETRIEVALS=10
        self.SLEEP_TIME=30
        self.DELEGATION_OPTIONS=''
        self.DEFAULTREQ=''
        self.NOPROXY=-1
        self.LOGFILE=''
        self.PROXY=''
        self.TMPFILE=''
        self.COMMANDEXITSTATUS=''
        self.TESTRESULT=-1
        self.logger=''
        self.TAGREQ='ALL'
        self.PRODUCTREQ=''
        self.STARTTIME=time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        self.ENDTIME=time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        
   def logger_setup(self):
        if self.LOGFILE == '' :
           print 'ERROR: No LOGFILE defined ! Exiting...'
           sys.exit(-1)

        logger1 = logging.getLogger('EMITestbed_PROCESSLOG') #put here the name of the function/main
        hdlr = logging.FileHandler(self.LOGFILE + '_PROCESS.log')
        formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
        hdlr.setFormatter(formatter)
        logger1.addHandler(hdlr)
        logger1.setLevel(logging.DEBUG)

   def loggerresults_setup(self):
        if self.LOGFILE == '' :
           print 'ERROR: No LOGFILE defined ! Exiting...'
           sys.exit(-1)

        logger2 = logging.getLogger('EMITestbed_RESULTLOG') #put here the name of the function/main
        hdlr2 = logging.FileHandler(self.LOGFILE + '_RESULTS.log')
        formatter = logging.Formatter('%(asctime)s   %(name)-20s :  %(levelname)-8s %(message)s','%Y-%m-%d %H:%M:%S')
        hdlr2.setFormatter(formatter)
        logger2.addHandler(hdlr2)
        logger2.setLevel(logging.DEBUG)

   
   def tagset_init(self,TAGLIST=['ALL']):
    #macro to initialize tagset
      try:
             self.logger.debug(" Initializing tagset")
             tagset=set()
             for tag in TAGLIST:
                tagset.add(tag)
             return tagset
      except Exception,e:
             self.logger.error('Error while initializing tagset. \tException:' + str(e) )
             return -1


   def check_proxy(self):
   #CHECK Existence of proxy for given VO
      try:
	     self.logger.debug(" Checking voms proxy existence")
	     command=str(self.UTILS_CLI['VOMS']['PROXYCHECK'])
	     self.logger.debug("Executing command:" + command)
	     OUTPUT=self.run_command(command)
             if str(OUTPUT[1].strip()) != str(self.TESTBED['VOMS']['VO']):
                self.logger.error('A valid proxy with 6 h time duration for VO ' + str(self.TESTBED['VOMS']['VO']) + ' is required to run tests.\tValid proxy not found, exiting')
                raise NameError('Proxy VO detected: ' + str(OUTPUT[1]) + ' does not match the expected VOMS: ' + str(self.TESTBED['VOMS']['VO']))
	     self.logger.debug("Command Output:" + str(OUTPUT[1]))
             return 0
      except Exception,e:
             self.logger.error('A valid proxy for VO ' + str(self.TESTBED['VOMS']['VO']) + ' is required to run tests.\tException:' + str(e) )
             return -1

   
   def run_command(self,args,fail=0):
   # Run command "args", if "fail" is set we expect a command failure (ret code != 0)
   # If command fails (or if "fail"=1 and it not fails), exit with failure 
   # returns command's output
        self.logger.debug('Run command: %s'%(args))
        OUTPUT=commands.getstatusoutput(args)
        if fail==0 and OUTPUT[0]!=0 :
            raise  NameError('Command %s failed. Failure message:' %args)
        elif fail==1 and OUTPUT[0]==0:
            raise NameError('Command %s not failed as expected.' %args)
        self.logger.info('Command output:\n' + OUTPUT[1])
        if fail==0:
            self.logger.debug('Command success')
        else:
            self.logger.debug('Command successfully failed')
        return OUTPUT
       
   def atomic_test_exec_report(self,product,testtag,testdescription,command):
      # Report test result 
      self.logger.debug("PROD=" + product + " | TESTTAG=" + testtag + " | TESTDESCRIPTION=" + testdescription)
      self.loggerresults.info("PROD=" + product + " | TESTTAG=" + testtag + " | TESTDESCRIPTION=" + testdescription)
      self.logger.debug("Executing command:\t" + command)
      OUTPUT=self.run_command(command)
      self.logger.debug("Command Output:\t" + str(OUTPUT[1]))
      if OUTPUT[0]==0:
         self.loggerresults.info("RESULT: SUCCESS")
         self.loggerresults.info("Command output+++++:\n" + str(OUTPUT[1]))
      else:
         self.loggerresults.info("RESULT: FAIL")
         self.loggerresults.info("Command output+++++:\n" + str(OUTPUT[1]))
      return OUTPUT[0]

   def jobsubmit_test_exec_report(self,product,testtag,testdescription,command):
      # Report test result 
      self.logger.debug("PROD=" + product + " | TESTTAG=" + testtag + " | TESTDESCRIPTION=" + testdescription)
      self.loggerresults.info("PROD=" + product + " | TESTTAG=" + testtag + " | TESTDESCRIPTION=" + testdescription)
      self.logger.debug("Executing command:\t" + command)
      OUTPUT=self.run_command(command)
      self.logger.debug("Command Output:\t" + str(OUTPUT[1]))
      if OUTPUT[0]==0:
         self.loggerresults.info("RESULT: SUCCESS")
         self.loggerresults.info("Command output+++++:\n" + str(OUTPUT[1]))
      else:
         self.loggerresults.info("RESULT: FAIL")
         self.loggerresults.info("Command output+++++:\n" + str(OUTPUT[1]))
      return (OUTPUT[0],OUTPUT[1])

   def waituntilterminalstatus_test_exec_report(self,product,testtag,testdescription,command,terminalstata,expectedstatus):
      # Report test result 
      'outputcondition must be a string which we expect to find in the output'
      self.logger.debug("PROD=" + product + " | TESTTAG=" + testtag + " | TESTDESCRIPTION=" + testdescription)
      self.loggerresults.info("PROD=" + product + " | TESTTAG=" + testtag + " | TESTDESCRIPTION=" + testdescription)
      self.logger.debug("Executing command:\t" + command)
      OUTPUT=self.run_command(command)
      self.logger.debug("Command Output:\t" + str(OUTPUT[1]))
      counter = 0

      terminalflag=0
      while (OUTPUT[0] ==0) and terminalflag==0 :
            if counter >= int(self.NUM_STATUS_RETRIEVALS) :
                self.logger.debug("Timeout reached while waiting the job to finish")  
                raise  NameError("Timeout reached while waiting the job to finish")
            self.logger.debug('*INFO* Jobstatus ... sleeping %s seconds ( %s/%s )'%(self.SLEEP_TIME,counter,self.NUM_STATUS_RETRIEVALS))
            time.sleep(int(self.SLEEP_TIME))
            counter=counter+1
            OUTPUT=self.run_command(command)
            self.logger.debug("Command Output:\t" + str(OUTPUT[1]))
            for x in terminalstata:
                if OUTPUT[1].find(x)!=-1:
                   self.logger.debug("Job in terminal status")
                   terminalflag=1
                   break
         
      if OUTPUT[0] == 0 :   
         if OUTPUT[1].find(expectedstatus) != -1 :
             self.loggerresults.info("RESULT: SUCCESS")
             self.loggerresults.info("Command output+++++:\n" + str(OUTPUT[1]))
         else :
             self.loggerresults.info("RESULT: FAIL")
             self.loggerresults.info("Command output+++++:\n" + str(OUTPUT[1]))
      else:
         self.loggerresults.info("COMMAND FAILS")
         self.loggerresults.info("Command output+++++:\n" + str(OUTPUT[1]))
      return OUTPUT[0]
