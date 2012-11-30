import sys
import os
import time
import sets

class WMS:
   '''Class implementing basic integration tests for product: WMS  '''

   def __init__(self,conf):
      self.PRODUCT = 'WMS'    
      self.NUMHOST = len(conf.TESTBED['WMS']['RESOURCES'])
      self.JOBID = []
      self.TERMINALSTATA=['DONE','ABORTED']
      self.EXPECTEDSTATA='DONE'

 
   def run_test(self,conf):
       
      try:
          TAGTEST1=conf.tagset_init(['INTEGRATION','UI'])
          if TAGTEST1==-1:
             raise NameError("Unable to initialize tagset")
          if conf.TAGREQ.issuperset(['ALL']) or (len(TAGREQ.intersection(TAGTEST1))>0) :
             
             try: 
			        # TEST1> Submission
		    for iresource in range(0,self.NUMHOST):                     
			command=str(conf.UTILS_CLI['WMS']['SUBMIT'])
			command=command.replace('ENDPOINT',str(conf.TESTBED['WMS']['RESOURCES'][iresource]))
			command=command.replace('JDL',str(conf.CONFFILES['BASICJDL']))
			(result, jobid)=conf.jobsubmit_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1: Job submission",command)
			if result==0:
			   self.JOBID.append(jobid.strip())
			else:
			   raise NameError("Unable to submit job, resource problem: " + str(conf.TESTBED['WMS']['RESOURCES'][iresource]))
			   conf.logger.error('Unable to submit job to WMS, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e))           
	     except Exception, e:
			        conf.logger.error('Unable to run WMS_TEST1, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

             try:
                    # TEST2
                    for ijobid in self.JOBID:
                        command=str(conf.UTILS_CLI['WMS']['JOBSTATUS'])
                        command=command.replace('JOBID',ijobid)
                        result=conf.waituntilterminalstatus_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2: WMS Job status",command,self.TERMINALSTATA,self.EXPECTEDSTATA)
             except Exception,e:
                    conf.logger.error('Unable to run WMS_TEST2 TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + self.PRODUCT + '\t Excepion:' + str(e) )
        return -1
        
   def ckeck_environment(self,conf):

      #This method is meant to check testing enviroment before running the test
      try:
          conf.logger.debug(" CHECKING resources: ")
          for iresource in range(0,self.NUMHOST):
	             try:
		             conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['WMS']['RESOURCES'][iresource].split('/')[2].split(':')[0]))
		             command=str(conf.UTILS_CLI['WMS']['CHECK'])
		             command=command.replace('ENDPOINT',str(conf.TESTBED['WMS']['RESOURCES'][iresource].split('/')[2].split(':')[0]))
		             conf.logger.info("Executing command:" + command)
		             OUTPUT=conf.run_command(command)
		             if OUTPUT[0] != 0 or  OUTPUT[1] != 1 :
			             conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['WMS']['RESOURCES'][iresource]))
			             return -1
	             except Exception,e:
		             conf.logger.error('TESTBED problem for WMS TEST, TAGS : ' + str(conf.TAGREQ) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to check test environment for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        return -1


