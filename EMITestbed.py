#!/usr/bin/python
import sys
import os
import time
sys.path.append('./LIB/')
import common_conf
import optparse 
import imp
import logging

if __name__=="__main__":
     conf=common_conf.commonconf()
     use = "This is the main function to run the basic battery of tests for EMI Integration  of GLITE components\nUsage: %prog [options] PRODUCT \n...where PRODUCT with relative tags must be among:\n"
     parser = optparse.OptionParser()
     for key in  conf.PRODUCTS.keys():
        use += key + ' : ' + str(conf.PRODUCTS[key]) + '\n'
     parser.add_option("-t", "--testtag", dest="TAGSET", action="store", default= "ALL", help="TAG of subset of tests to run")
     parser.add_option("-f", "--file", dest="OutFilename", action="store", default=conf.STARTTIME , help="Write output to specified filepath", metavar="FILE")
     (options, args) = parser.parse_args()

     #SETUP CHECKS
     if len(args) != 1:
        parser.error(use)
     if conf.PRODUCTS.has_key(args[0]) == False :
        parser.error(use)
     else:
        conf.PRODUCTREQ=args[0]
     if options.TAGSET:  
        if (options.TAGSET in conf.PRODUCTS[args[0]] == False):
           parser.error(use)
        else:
           conf.TAGREQ=options.TAGSET
     else:
        conf.TAGREQ = set(['ALL'])
     
     #INITIALIZATION
     conf.LOGFILE=options.OutFilename
     conf.logger_setup()
     conf.logger=logging.getLogger('EMITestbed_PROCESSLOG')
     conf.logger.info('++++++++++++++++++++++++++++++++++++++++++++++++++')
     conf.logger.info('Starting the test for product:' + conf.PRODUCTREQ )
     conf.logger.info('Will execute tests matching TAG:' + conf.TAGREQ )
     conf.loggerresults_setup()
     conf.loggerresults=logging.getLogger('EMITestbed_RESULTLOG')
     conf.loggerresults.info('++++++++++++++++++++++++++++++++++++++++++++++++++')
     conf.loggerresults.info('Starting the test for product:' + conf.PRODUCTREQ )
     conf.loggerresults.info('Test started at: ' + self.STARTTIME)
     conf.loggerresults.info('Will execute tests matching TAG:' + conf.TAGREQ )

     try:
        module = __import__(conf.PRODUCTREQ + '_class')
        class_ = getattr(module,conf.PRODUCTREQ)
        testclass = class_(conf)
     except Exception,e:
        conf.logger.error('Unable to instantiate testclass for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        sys.exit(-1)

     #CHECK PROXY EXISTENCE

     #TODO!!!!!!!!!!!


     #RUNNING TEST   
     try:
        conf.logger.info('Running test')       
        testclass.run_test() 
     except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        sys.exit(-1)

     #CHECKING RESULTS
     try:
	conf.logger.info('Checking results')                                               
        testclass.ckeck_results()
     except Exception,e:
        conf.logger.error('Unable to check results for considered product test: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        sys.exit(-1)

     self.ENDTIME=time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
     conf.logger.info('Test completed at: ' + self.ENDTIME)
     conf.loggerresults.info('Test completed at: ' + self.ENDTIME)
     conf.logger.info('++++++++++++++++++++++++++++++++++++++++++++++++++')