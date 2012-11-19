import sys
import os
import time
import common
import set

class LFC(conf):

   '''Class implementing basic integration tests for product: LFC
      Input args: 
       - CONFFILES : Dictionary including path of files needed for tests
       - TESTBED   : Dictionary including hosts endpoints for all products involved in the tests and relative conf info
       - UTILS_CLI : Dictionary including cli commands available on UI to test productspath of files needed for tests
       - TAGSET    : Set of TAGS defined for available tests ('ALL') is default  
   '''

   def __init__(self):
      self.PRODUCT = 'LFC'    
      self.NUMHOST = len(TESTBED['LFC']['RESOURCES'])
      
   def run_test(self):
       
      try:
          TAGTEST1=set(['INTEGRATION'])
          if conf.TAGREQ.issuperset(['ALL']) or (len(TAGSET.intersection(TAGTEST1))>0) :
             for iresources in range(0,self.NUMHOST):
                     try: 
			     # TEST1
			     conf.logger.info(" LFC_TEST1, TAGS : " + str(TAGTEST1))
			     conf.logger.info(" LFC_TEST : listing directory")
			     command=str(conf.UTILS_CLI['LFC']['LS'])
			     command=command.replace('ENDPOINT',str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
			     command=command.replace('DESTPATH',str(conf.TESTBED['LFC']['VODIR'][iresource]))
			     conf.logger.info("Executing command:" + command)
			     OUTPUT=conf.run_command(command)
			     conf.logger.info("Command Output:" + OUTPUT) 
		     except Exception,e:
			     conf.logger.error('Unable to run LFC_TEST1, TAGS : ' + str(TAGTEST1) '\tException:' + str(e) )
			    
                     try:
			     # TEST2
			     conf.logger.info(" LFC_TEST2, TAGS : " + str(TAGTEST1))
			     conf.logger.info(" LFC_TEST : directory creation")
			     command=str(conf.UTILS_CLI['LFC']['MKDIR'])
			     command=command.replace('ENDPOINT',str(conf.TESTBED['LFC']['RESOURCES'][iresource]))
			     destination = str(conf.TESTBED['LFC']['VODIR'][iresource]) + '/' + str(conf.TESTBED['LFC']['DESTPATH'][iresource])
			     command=command.replace('DESTPATH',destination)
			     conf.logger.info("Executing command:" + command)
			     OUTPUT=conf.run_command(command)
			     conf.logger.info("Command Output:" + OUTPUT)
                     except Exception,e:
                             conf.logger.error('Unable to run LFC_TEST2, TAGS : ' + str(TAGTEST1) '\tException:' + str(e) )
 

      except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        return -1
        



   def ckeck_results(self):

       try:
          TAGTEST1=set(['INTEGRATION'])
          if conf.TAGREQ.issuperset(['ALL']) or (len(TAGSET.intersection(TAGTEST1))>0) :
             for iresources in range(0,self.NUMHOST):
                     try:
                             # TEST1
                             conf.loggerresults.info(" CHECK RESULTS FOR LFC_TEST1, TAGS : " + str(TAGTEST1))
                             conf.loggerresults.info(" CHECK RESULTS FOR LFC_TEST : listing directory")
                             conf.loggerresults.info(" TEST OK" )
                     except Exception,e:
                             conf.logger.error('Unable to check LFC_TEST1, TAGS : ' + str(TAGTEST1) '\tException:' + str(e) )
                             conf.loggerresults.error(" TEST FAILS" )

                            
                     try:
                             # TEST2
                             conf.logger.info(" CHECK RESULTS FOR LFC_TEST2, TAGS : " + str(TAGTEST1))
                             conf.logger.info(" CHECK RESULTS FOR LFC_TEST : listing directory")
                             conf.logger.info(" TEST OK" )
                     except Exception,e:
                             conf.logger.error('Unable to run LFC_TEST2, TAGS : ' + str(TAGTEST1) '\tException:' + str(e) )
                             conf.loggerresults.error(" TEST FAILS" )


      except Exception,e:
        conf.logger.error('Unable to check test results for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        return -1


