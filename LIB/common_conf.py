import os
import sys
import time
import commands
import string
import logging
import datetime 
from exceptions import *

class commonconf:

   def __init__(self):
        #INITIALIZATION GLOBAL CONFIGURATION
        self.PRODUCTS  = { # 'PRODUCT NAME' : ['TAG1', 'TAG2'],
                                      'LFC' : ['INTEGRATION'], 
                                      'DPM' : ['INTEGRATION'],
                                   'DCACHE' : ['INTEGRATION'],
                                    'CREAM' : ['INTEGRATION'],
                                      'WMS' : ['INTEGRATION'],
                                   'WNODES' : ['INTEGRATION'],
                                 'CREAMMPI' : ['INTEGRATION'],
                                 'LCGUTILS' : ['INTEGRATION'],
                                    'STORM' : ['INTEGRATION']
                         }
        self.CONFFILES = {      'CEoutfile' : '../OUT/CEoutfile.txt',
                                'MPIJDL'    : '../JDL/mpitest.jdl',
                                'BASICJDL'  : '../JDL/basictest.jdl',
                             'CEMPIoutfile' : '../OUT/CEMPIoutfile.txt',
                               'WMSoutfile' : '../OUT/WMSoutfile.txt',
                               'SOURCEFILE' : '../JDL/basictest.jdl'
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
                                      'DESTPATH': ['destpathtest/file1', 'destpathtest/file1']
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
                                    
                        'DCACHE' : {'RESOURCES': ['cork.desy.de']
                                   },
                                   
                           'LFC' : {'RESOURCES': ['emi2rc-sl5-lfc.cern.ch:/grid/testers.eu-emi.eu/'],
                                     'TESTDIR': ['destpathtest']
                                   },
                        
                           'DPM' : {'RESOURCES': ['lxbra1910.cern.ch']
                                   }
                          }
        self.UTILS_CLI  = {       'CREAM'  :  {      'SUBMIT' : 'glite-ce-job-submit -d  -r ENDPOINT -a JDL',
                                                               'JOBSTATUS' : 'glite-ce-job-status JOBID'
                                              },
                                     'WMS' :  {                   'SUBMIT' : 'glite-wms-job-submit -d  -r ENDPOINT -a JDL',
                                                               'JOBSTATUS' : 'glite-wms-job-status JOBID'
                                              },
                                     'SRM' :  {                     'PING' : 'clientSRM ping -e httpg://ENDPOINT:8444',
                                                                  'MKDIR'  : 'srmmkdir -2 -debug srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                                      'RM' : 'srmrm  srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                                   'RMDIR' : 'srmrmdir  srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH'  
                                              },
                                  'GLOBUS' :  {                      'GUC' : 'globus-url-copy file://`pwd`/TESTFILE   gsiftp://ENDPOINT:2811/DESTPATH' 
                                              },
                                    'LDAP' :  {           'SEARCHRESOURCE' : 'ldapsearch -x -H ldap://ENDPOINT:2170/ -b mds-vo-name=resource,o=grid',
                                                           'SEARCHTOPBDII' : 'ldapsearch -x -H  ldap://BDII_TOP -b mds-vo-name=local,o=grid',
                                                          'SEARCHSITEBDII' : 'ldapsearch -x -H  ldap://BDII_SITE -b mds-vo-name=BDII_SITE_NAME,o=grid' ,
                                                         'SEARCH_SITE_OBJ' : "ldapsearch -x -H  ldap://BDII_SITE -b mds-vo-name=BDII_SITE_NAME,o=grid 'objectclass: GlueTop' "
                                              },
                                'LCGUTILS' :  {                       'LS' : 'lcg-ls -v -l -b -D srmv2 srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                                      'CP' : 'lcg-cp -b --verbose -D srmv2 file://SOURCEPATH`pwd`/TESTFILE srm://ENDPOINT:8444/srm/managerv2?SFN=/DESTPATH',
                                                               'INFOSITES' : 'lcg-infosites --vo VOMS all',
                                                            'INFOSITES_CE' : 'lcg-infosites --vo VOMS ce',
                                                            'INFOSITES_SE' : 'lcg-infosites --vo VOMS se',
                                                               'INFO_CE'   : 'lcg-info --list-ce --vo VOMS',
                                                               'INFO_SE'   : 'lcg-info --list-se --vo VOMS'
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
        self.NUM_STATUS_RETRIEVALS=120
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
   #     self.logger.debug('Run command: %s'%(args))
        OUTPUT=commands.getstatusoutput(args)
        if fail==0 and OUTPUT[0]!=0 :
   #         self.logger.error('Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
            raise  NameError('Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
        elif fail==1 and OUTPUT[0]==0:
   #         self.logger.error('Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
            raise NameError('Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
   #     self.logger.info('Command output:\n%s'%OUTPUT[1],'DEBUG')
        if fail==0:
            self.logger.debug('Command success')
        else:
            self.logger.debug('Command successfully failed')
        return OUTPUT
        
   def run_command_until(self,args,condition,fail=0):
    # Run command "args", if "fail" is set we expect a command failure (ret code != 0)
    # If command fails (or if "fail"=1 and it not fails), exit with failure 
    # returns command's output
        self.logger.debug('Run command: %s'%(args))
        OUTPUT=commands.getstatusoutput(args)
        if fail==0 and OUTPUT[0]!=0 :
            self.logger.error('Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
            raise NameError('Command %s failed. Failure message: %s'%(args,OUTPUT[1]))
        elif fail==1 and OUTPUT[0]==0:
            self.logger.error('Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
            raise NameError('','Command %s not failed as expected. Command output: %s'%(args,OUTPUT[1]))
        self.logger.debug('Command output:\n%s'%(OUTPUT[1]),'DEBUG')
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

