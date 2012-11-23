import sys
import os
import time
import sets

class LFC:
   '''Class implementing basic integration tests for product: LFC
      Input args: 
       - CONFFILES : Dictionary including path of files needed for tests
       - TESTBED   : Dictionary including hosts endpoints for all products involved in the tests and relative conf info
       - UTILS_CLI : Dictionary including cli commands available on UI to test productspath of files needed for tests
       - TAGSET    : Set of TAGS defined for available tests ('ALL') is default  
   '''

   def __init__(self,conf):
      self.PRODUCT = 'LFC'    
      self.NUMHOST = len(conf.TESTBED['LFC']['RESOURCES'])
      
   def run_test(self,conf):
       
      try:
          TAGTEST1=set()
          TAGTEST1.add('INTEGRATION')
          if conf.TAGREQ.issuperset(['ALL']) or (len(TAGREQ.intersection(TAGTEST1))>0) :
             for iresource in range(0,self.NUMHOST):
                     try: 
			     # TEST1
                             command=str(conf.UTILS_CLI['LFC']['LS'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1: listing directory",command)
		     except Exception,e:
			     conf.logger.error('Unable to run LFC_TEST1, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )
			    
                     try:
			     # TEST2
			     command=str(conf.UTILS_CLI['LFC']['MKDIR'])
			     command=command.replace('ENDPOINT',str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
			     command=command.replace('TESTDIR','/' + str(conf.TESTBED['LFC']['TESTDIR'][iresource]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2: directory creation",command)
                     except Exception,e:
                             conf.logger.error('Unable to run LFC_TEST2, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

                     try:
                             # TEST3
                             command=str(conf.UTILS_CLI['LFC']['RMDIR'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
                             command=command.replace('TESTDIR','/' + str(conf.TESTBED['LFC']['TESTDIR'][iresource]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3: directory deletion",command)
                     except Exception,e:
                             conf.logger.error('Unable to run LFC_TEST3 TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + self.PRODUCT + '\t Excepion:' + str(e) )
        return -1
        
   def ckeck_environment(self,conf):

      #This method is meant to check testing enviroment before running the test
      try:
          conf.logger.debug(" CHECKING resources: ")
          for iresource in range(0,self.NUMHOST):
	     try:
		     conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
		     command=str(conf.UTILS_CLI['LFC']['LS'])
		     command=command.replace('ENDPOINT',str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
		     conf.logger.info("Executing command:" + command)
		     OUTPUT=conf.run_command(command)
		     if OUTPUT[0] != 0:
			conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
			raise NameError("Unreachable resource problem: " + str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
			return -1
	     except Exception,e:
		     conf.logger.error('TESTBED problem for LFC TEST, TAGS : ' + str(conf.TAGREQ) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to check test environment for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        return -1


