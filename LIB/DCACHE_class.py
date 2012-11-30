import sys
import os
import time
import sets

class DCACHE:
   '''Class implementing basic integration tests for product: DCACHE
      Input args: 
       - CONFFILES : Dictionary including path of files needed for tests   '''

   def __init__(self,conf):
      self.PRODUCT = 'DCACHE'    
      self.NUMHOST = len(conf.TESTBED['DCACHE']['RESOURCES'])
      
   def run_test(self,conf):
       
      try:

          TAGTEST1=conf.tagset_init(['INTEGRATION','UI'])
          if TAGTEST1==-1:
             raise NameError("Unable to initialize tagset")

          if conf.TAGREQ.issuperset(['ALL']) or (len(TAGREQ.intersection(TAGTEST1))>0) :
             for iresource in range(0,self.NUMHOST):

			    
                     try:
                             # TEST1
                             conf.logger.debug(" LS TEST: " + str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
                             command=str(conf.UTILS_CLI['SRM']['LS'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
                             command=command.replace('VODIR',str(conf.TESTBED['DCACHE']['VODIR'][iresource]))
                             conf.logger.info("Executing command:" + command)
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3: LS VODIR",command)
                     except Exception,e:
                             conf.logger.error('Unable to run DCACHE_TEST1, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )


                     try:
                             # TEST2
			     #CP FILE
                             conf.logger.debug(" SRM CP TEST: " + str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
                             command=str(conf.UTILS_CLI['SRM']['CP'])
                             command=command.replace('TESTFILE',str(conf.CONFFILES['BASICJDL']))
                             command=command.replace('ENDPOINT',str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
                             command=command.replace('VODIR',str(conf.TESTBED['DCACHE']['VODIR'][iresource])  + '/')
                             command=command.replace('DESTFILE',str(conf.CONFFILES['BASICJDL'].split('/')[2] ))
                             conf.logger.info("Executing command:" + command)
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST5: CP FILE to Created Directory",command)

                             #RM FILE
                             command=str(conf.UTILS_CLI['SRM']['RM'])
                             command=command.replace('ENDPOINT', str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
                             command=command.replace('VODIR',str(conf.TESTBED['DCACHE']['VODIR'][iresource])  + '/')
                             command=command.replace('DESTPATH', str(conf.CONFFILES['BASICJDL'].split('/')[2]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST5: RM file from directory ",command)

                     except Exception,e:
                             conf.logger.error('Unable to run DCACHE_TEST5, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + self.PRODUCT + '\t Excepion:' + str(e) )
        return -1
        
   def ckeck_environment(self,conf):

      #This method is meant to check testing enviroment before running the test
      try:
          conf.logger.debug(" CHECKING resources: ")
          for iresource in range(0,self.NUMHOST):
	     try:
		     conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
		     command=str(conf.UTILS_CLI['SRM']['PING'])
		     command=command.replace('ENDPOINT',str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
		     conf.logger.info("Executing command:" + command)
		     OUTPUT=conf.run_command(command)
		     if OUTPUT[0] != 0:
			conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
			raise NameError("Unreachable resource problem: " + str(conf.TESTBED['DCACHE']['RESOURCES'][iresource]))
			return -1
	     except Exception,e:
		     conf.logger.error('TESTBED problem for DCACHE TEST, TAGS : ' + str(conf.TAGREQ) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to check test environment for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        return -1


