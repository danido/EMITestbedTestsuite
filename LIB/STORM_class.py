import sys
import os
import time
import sets

class STORM:
   '''Class implementing basic integration tests for product: STORM
      Input args: 
       - CONFFILES : Dictionary including path of files needed for tests   '''

   def __init__(self,conf):
      self.PRODUCT = 'STORM'    
      self.NUMHOST = len(conf.TESTBED['STORM']['RESOURCES'])
      
   def run_test(self,conf):
       
      try:

          TAGTEST1=conf.tagset_init(['INTEGRATION','UI'])
          if TAGTEST1==-1:
             raise NameError("Unable to initialize tagset")

          if conf.TAGREQ.issuperset(['ALL']) or (len(TAGREQ.intersection(TAGTEST1))>0) :
             for iresource in range(0,self.NUMHOST):

                     try: 
			     # TEST1
                             command=str(conf.UTILS_CLI['GLOBUS']['GUC'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=command.replace('TESTFILE',str(conf.CONFFILES['BASICJDL']))
                             command=command.replace('DESTPATH',str(conf.TESTBED['STORM']['DESTGUCPATH'][iresource]+str(time.time())))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST1: globus url copy",command)
		     except Exception,e:
			     conf.logger.error('Unable to run STORM_TEST1, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )
			    
                     try:
			     # TEST2
                             conf.logger.debug(" CHECKING UBERFTP ON  resource: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=str(conf.UTILS_CLI['WMS']['CHECK'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             conf.logger.info("Executing command:" + command)
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST2: uberftp",command)
                     except Exception,e:
                             conf.logger.error('Unable to run STORM_TEST2, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

                     try:
                             # TEST3
                             conf.logger.debug(" LS TEST: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=str(conf.UTILS_CLI['LCGUTILS']['LS_SRM'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=command.replace('DESTPATH',str(conf.TESTBED['STORM']['VODIR'][iresource]))
                             conf.logger.info("Executing command:" + command)
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST3: LS VODIR",command)
                     except Exception,e:
                             conf.logger.error('Unable to run STORM_TEST3, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

                     try:
                             # TEST4
                             conf.logger.debug(" LDAP TEST: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=str(conf.UTILS_CLI['LDAP']['SEARCHRESOURCE'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=command + '|grep  ' + str(conf.TESTBED['STORM']['VODIR'][iresource])
                             conf.logger.info("Executing command:" + command)
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST4: LDAPSEARCH",command)
                     except Exception,e:
                             conf.logger.error('Unable to run STORM_TEST4, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

                     try:
                             # TEST5
                             #MKDIR
                             conf.logger.debug(" SRMMKDIR + FILE: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=str(conf.UTILS_CLI['SRM']['MKDIR'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=command.replace('DESTPATH', str(conf.TESTBED['STORM']['VODIR'][iresource]) + '/' + str(conf.TESTBED['STORM']['DESTPATH'][iresource].split('/')[0]))
                             conf.logger.info("Executing command:" + command)
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST5: MKDIR",command)
			     #CP FILE
                             conf.logger.debug(" LCG CP TEST: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=str(conf.UTILS_CLI['LCGUTILS']['CP_SRM'])
                             command=command.replace('TESTFILE',str(conf.CONFFILES['BASICJDL']))
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=command.replace('DESTPATH',str(conf.TESTBED['STORM']['VODIR'][iresource]) + '/' + str(conf.TESTBED['STORM']['DESTPATH'][iresource]))
                             conf.logger.info("Executing command:" + command)
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST5: CP FILE to Created Directory",command)
                             #RM FILE
                             command=str(conf.UTILS_CLI['SRM']['RM'])
                             command=command.replace('ENDPOINT', str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=command.replace('DESTPATH', str(conf.TESTBED['STORM']['VODIR'][iresource]) + '/' + str(conf.TESTBED['STORM']['DESTPATH'][iresource]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST5: RM file from directory ",command)
                             #RM DIR
                             command=str(conf.UTILS_CLI['SRM']['RMDIR'])
                             command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
                             command=command.replace('DESTPATH',str(conf.TESTBED['STORM']['VODIR'][iresource]) + '/' +  str(conf.TESTBED['STORM']['DESTPATH'][iresource].split('/')[0]))
                             result=conf.atomic_test_exec_report(self.PRODUCT,str(TAGTEST1),"TEST5: directory deletion",command)

                     except Exception,e:
                             conf.logger.error('Unable to run STORM_TEST5, TAGS : ' + str(TAGTEST1) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + self.PRODUCT + '\t Excepion:' + str(e) )
        return -1
        
   def ckeck_environment(self,conf):

      #This method is meant to check testing enviroment before running the test
      try:
          conf.logger.debug(" CHECKING resources: ")
          for iresource in range(0,self.NUMHOST):
	     try:
		     conf.logger.debug(" CHECKING resource: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
		     command=str(conf.UTILS_CLI['SRM']['PING'])
		     command=command.replace('ENDPOINT',str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
		     conf.logger.info("Executing command:" + command)
		     OUTPUT=conf.run_command(command)
		     if OUTPUT[0] != 0:
			conf.logger.error("Unreachable resource problem: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
			raise NameError("Unreachable resource problem: " + str(conf.TESTBED['STORM']['RESOURCES'][iresource]))
			return -1
	     except Exception,e:
		     conf.logger.error('TESTBED problem for STORM TEST, TAGS : ' + str(conf.TAGREQ) + '\tException:' + str(e) )

      except Exception,e:
        conf.logger.error('Unable to check test environment for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        return -1


