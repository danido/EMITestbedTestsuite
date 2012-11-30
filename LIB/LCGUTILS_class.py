import sys
import os
import time
import sets

class LCGUTILS:
   '''Class implementing basic integration tests for product: LCGUTILS
      Input args: 
       - CONFFILES : Dictionary including path of files needed for tests   '''

   def __init__(self,conf):
      self.PRODUCT = 'LCGUTILS'    
      
   def run_test(self,conf):
       
      try:

          TAGTEST1=conf.tagset_init(['INTEGRATION','UI'])
          if TAGTEST1==-1:
             raise NameError("Unable to initialize tagset")

          if conf.TAGREQ.issuperset(['ALL']) or (len(TAGREQ.intersection(TAGTEST1))>0) :
                     try: 
			     # TEST1:INFOSITES
                             command=str(conf.UTILS_CLI['LCGUTILS']['INFOSITES'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.1: infosites all",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['INFOSITES_CE'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.2: infosites ce",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['INFOSITES_SE'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.3: infosites se",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['INFOSITES_BDIITOP'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.4: bdii top",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['INFOSITES_BDIISITE'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.5: infosites bdii site",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['INFO_CE'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.6: info ce",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['INFO_SE'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.7: info se",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['INFO_SE_ATTR_NAME'])
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1.8: info se attr name",command)

		     except Exception,e:
			     conf.logger.error('Unable to run LCGUTILS_TEST1, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )
			    
                     try:
			     # TEST2:LDAPSEARCH BDII
			     command=str(conf.UTILS_CLI['LDAP']['SEARCHTOPBDII'])
			     command=command.replace('BDII_TOP',str(conf.TESTBED['BDII_TOP']['RESOURCES']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2.1: LDAP TOP BDII ",command)

                             command=str(conf.UTILS_CLI['LDAP']['SEARCHSITEBDII'])
                             command=command.replace('BDII_SITE',str(conf.TESTBED['BDII_SITE']['RESOURCES']))
                             command=command.replace('SITE_NAME',str(conf.TESTBED['BDII_SITE']['SITE_NAME']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2.2: LDAP SITE BDII ",command)

                             command=str(conf.UTILS_CLI['LDAP']['SEARCH_SITE_OBJ'])
                             command=command.replace('BDII_SITE',str(conf.TESTBED['BDII_SITE']['RESOURCES']))
                             command=command.replace('SITE_NAME',str(conf.TESTBED['BDII_SITE']['SITE_NAME']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2.3: LDAP SITE BDII OBJ ",command)
                     except Exception,e:
                             conf.logger.error('Unable to run LCGUTILS_TEST2, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

                     try:
                             # TEST3: REPLICAS
                             command=str(conf.UTILS_CLI['LCGUTILS']['CR_LFN'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             command=command.replace('DESTFILE',str(conf.CONFFILES['BASICJDL'].split('/')[2]))
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][0]))
                             command=command.replace('TESTFILE',str(conf.CONFFILES['BASICJDL']))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3.1: registering lfn",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['LR_LFN'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             command=command.replace('TESTFILE',str(conf.CONFFILES['BASICJDL'].split('/')[2]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3.2: list replicas lfn",command)

                             command=str(conf.UTILS_CLI['LCGUTILS']['DEL_LFN'])
                             command=command.replace('VOMS',str(conf.TESTBED['VOMS']['VO']))
                             command=command.replace('TESTFILE',str(conf.CONFFILES['BASICJDL'].split('/')[2]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3.3: delete replicas lfn",command)
                     except Exception,e:
                             conf.logger.error('Unable to run LCGUTILS_TEST3 TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + self.PRODUCT + '\t Excepion:' + str(e) )
        return -1
        
   def ckeck_environment(self,conf):

      #This method is meant to check testing enviroment before running the test
      try:
          conf.logger.debug(" CHECKING resources: ")
          conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['STORM']['RESOURCES'][0]))
          command=str(conf.UTILS_CLI['SRM']['PING'])
          command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][0]))
          conf.logger.info("Executing command:" + command)
          OUTPUT=conf.run_command(command)
          if OUTPUT[0] != 0:
             conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['STORM']['RESOURCES'][0]))
             raise NameError("Unreachable resource problem: " + str(conf.TESTBED['STORM']['RESOURCES'][0]))
             return -1
      except Exception,e:
          conf.logger.error('Unable to check test environment for considered product (STORM ENDPOINT): '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
          return -1


