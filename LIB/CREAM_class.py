import sys
import os
import time
import sets

class CREAM:
   '''Class implementing basic integration tests for product: CREAM  '''

   def __init__(self,conf):
      self.PRODUCT = 'CREAM'    
      self.NUMHOST = len(conf.TESTBED['CREAMCE']['RESOURCES'])
      self.NUMHOSTMPI = len(conf.TESTBED['CREAMCE_MPI']['RESOURCES'])
      self.JOBID = []
      self.JOBIDMPI = []
      self.TERMINALSTATA=['DONE-OK','ABORTED','DONE-FAILED','CANCELLED']
      self.EXPECTEDSTATA='DONE-OK'
      
   def run_test(self,conf):
       
      try:
          TAGTEST1=conf.tagset_init(['INTEGRATION','UI','CREAM'])
          if TAGTEST1==-1:
             raise NameError("Unable to initialize tagset")

          if conf.TAGREQ.issuperset(['ALL']) or (len(conf.TAGREQ.intersection(TAGTEST1))>0) :
             
             try: 
			        # TEST1> Submission
		    for iresource in range(0,self.NUMHOST):                     
			command=str(conf.UTILS_CLI['CREAM']['SUBMIT'])
			command=command.replace('ENDPOINT',str(conf.TESTBED['CREAMCE']['RESOURCES'][iresource]))
			command=command.replace('JDL',str(conf.CONFFILES['BASICJDL']))
			(result, jobid)=conf.jobsubmit_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1: Job submission",command)
			if result==0:
			   self.JOBID.append(jobid.strip())
			else:
			   raise NameError("Unable to submit job, resource problem: " + str(conf.TESTBED['CREAMCE']['RESOURCES'][iresource]))
			   conf.logger.error('Unable to submit job to CREAMCE, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e))           
	     except Exception, e:
			        conf.logger.error('Unable to run CREAMCE_TEST1, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

             try:
                    # TEST1 CHECK
                    for ijobid in self.JOBID:
                        command=str(conf.UTILS_CLI['CREAM']['JOBSTATUS'])
                        command=command.replace('JOBID',ijobid)
                        result=conf.waituntilterminalstatus_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1 CHECK: CREAM Job status",self.TERMINALSTATA,self.EXPECTEDSTATA)
             except Exception,e:
                    conf.logger.error('Unable to run CREAM_TEST1 CHECK TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

          TAGTEST1=conf.tagset_init(['INTEGRATION','UI','MPI'])
          if TAGTEST1 == -1:
             raise NameError("Unable to initialize tagset")

          if conf.TAGREQ.issuperset(['ALL']) or (len(conf.TAGREQ.intersection(TAGTEST1))>0) :

             try:
   		    # TEST 2 : CREAM MPI SUBMISSION
                    for iresource in range(0,self.NUMHOSTMPI):
                        command=str(conf.UTILS_CLI['CREAM']['SUBMIT'])
                        command=command.replace('ENDPOINT',str(conf.TESTBED['CREAMCE_MPI']['RESOURCES'][iresource]))
                        command=command.replace('JDL',str(conf.CONFFILES['MPIJDL']))
                        (result, jobid)=conf.jobsubmit_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2: MPI Job submission",command)
			conf.logger.info(jobid)
                        if result==0:
                           self.JOBIDMPI.append(jobid.strip())
                        else:
                           raise NameError("Unable to submit job, resource problem: " + str(conf.TESTBED['CREAMCE_MPI']['RESOURCES'][iresource]))
                           conf.logger.error('Unable to submit job to CREAMCE, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )
	     except Exception,e:
                           conf.logger.error('Unable to run CREAMCE_MPI_TEST2, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

             try:
                    # TEST2 CHECK
                    for ijobid in self.JOBIDMPI:
                        command=str(conf.UTILS_CLI['CREAM']['JOBSTATUS'])
                        command=command.replace('JOBID',ijobid)
                        result=conf.waituntilterminalstatus_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2: CREAMMPI CHECK Job status",command,self.TERMINALSTATA,self.EXPECTEDSTATA)
             except Exception,e:
                    conf.logger.error('Unable to run CREAM MPI TEST2 CHECK TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

          TAGTEST1=conf.tagset_init(['INTEGRATION','UI','WNODES'])
          if TAGTEST1==-1:
             raise NameError("Unable to initialize tagset")

          if conf.TAGREQ.issuperset(['ALL']) or (len(conf.TAGREQ.intersection(TAGTEST1))>0) :
             try:
                    # TEST 3 : CREAM WNODES SUBMISSION
                    for iresource in range(0,self.NUMHOSTMPI):
                        command=str(conf.UTILS_CLI['CREAM']['SUBMIT'])
                        command=command.replace('ENDPOINT',str(conf.TESTBED['WNODES']['RESOURCES'][iresource]))
                        command=command.replace('JDL',str(conf.CONFFILES['BASICJDL']))
                        (result, jobid)=conf.jobsubmit_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3: WNODES Job submission",command)
                        conf.logger.info(jobid)
                        if result==0:
                           self.JOBIDMPI.append(jobid.strip())
                        else:
                           raise NameError("Unable to submit job, resource problem: " + str(conf.TESTBED['WNODES']['RESOURCES'][iresource]))
                           conf.logger.error('Unable to submit job to WNODES, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )
             except Exception,e:
                           conf.logger.error('Unable to run WNODES_TEST3, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

             try:
                    # TEST3 CHECK
                    for ijobid in self.JOBIDMPI:
                        command=str(conf.UTILS_CLI['CREAM']['JOBSTATUS'])
                        command=command.replace('JOBID',ijobid)
                        result=conf.waituntilterminalstatus_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3: WNODES CHECK Job status",command,self.TERMINALSTATA,self.EXPECTEDSTATA)
             except Exception,e:
                    conf.logger.error('Unable to run WNODES TEST3 CHECK TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )


      except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + self.PRODUCT + '\t Excepion:' + str(e) )
        return -1

        
   def ckeck_environment(self,conf):

      #This method is meant to check testing enviroment before running the test
      try:
          conf.logger.debug(" CHECKING resources: ")
          for iresource in range(0,self.NUMHOST):
	             try:
			    #CREAM
		            TAGTEST1=conf.tagset_init(['INTEGRATION','UI','CREAM'])
		            if TAGTEST1==-1:
		               raise NameError("Unable to initialize tagset")
		            if conf.TAGREQ.issuperset(['ALL']) or (len(conf.TAGREQ.intersection(TAGTEST1))>0) :

		                conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['CREAMCE']['RESOURCES'][iresource].split('/')[0]))
		                command=str(conf.UTILS_CLI['CREAM']['SERVICEINFO'])
		                command=command.replace('ENDPOINT',str(conf.TESTBED['CREAMCE']['RESOURCES'][iresource].split('/')[0]))
		                conf.logger.info("Executing command:" + command)
   		                OUTPUT=conf.run_command(command)
   		                if OUTPUT[0] != 0:
			             conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['CREAMCE']['RESOURCES'][iresource]))
			             return -1
			    #CREAM_MPI
                            TAGTEST1=conf.tagset_init(['INTEGRATION','UI','MPI'])
                            if TAGTEST1==-1:
                               raise NameError("Unable to initialize tagset")
                            if conf.TAGREQ.issuperset(['ALL']) or (len(conf.TAGREQ.intersection(TAGTEST1))>0) :

                                conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['CREAMCE_MPI']['RESOURCES'][iresource].split('/')[0]))
                                command=str(conf.UTILS_CLI['CREAM']['SERVICEINFO'])
                                command=command.replace('ENDPOINT',str(conf.TESTBED['CREAMCE_MPI']['RESOURCES'][iresource].split('/')[0]))
                                conf.logger.info("Executing command:" + command)
                                OUTPUT=conf.run_command(command)
                                if OUTPUT[0] != 0:
                                     conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['CREAMCE']['RESOURCES'][iresource]))
                                     return -1
			    #WNODES
                            TAGTEST1=conf.tagset_init(['INTEGRATION','UI','WNODES'])
                            if TAGTEST1==-1:
                               raise NameError("Unable to initialize tagset")
                            if conf.TAGREQ.issuperset(['ALL']) or (len(conf.TAGREQ.intersection(TAGTEST1))>0) :

                                conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['CREAMCE_MPI']['RESOURCES'][iresource].split('/')[0]))
                                command=str(conf.UTILS_CLI['CREAM']['SERVICEINFO'])
                                command=command.replace('ENDPOINT',str(conf.TESTBED['CREAMCE_MPI']['RESOURCES'][iresource].split('/')[0]))
                                conf.logger.info("Executing command:" + command)
                                OUTPUT=conf.run_command(command)
                                if OUTPUT[0] != 0:
                                     conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['CREAMCE']['RESOURCES'][iresource]))
                                     return -1

	             except Exception,e:
		             conf.logger.error('TESTBED problem for CREAMCE TEST, TAGS : ' + str(conf.TAGREQ) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to check test environment for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        return -1


