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
     parser.add_option("-t", "--testtag", dest="TAGREQ", action="store", default= "ALL", help="TAG of subset of tests to run")
     parser.add_option("-f", "--file", dest="OutFilename", action="store", default=conf.STARTTIME , help="Write output to specified filepath", metavar="FILE")
     (options, args) = parser.parse_args()

     #SETUP CHECKS
     if len(args) != 1:
        parser.error(use)
     if conf.PRODUCTS.has_key(args[0]) == False :
        parser.error(use)
     else:
        conf.PRODUCTREQ=args[0]
     conf.TAGREQ=set()
     if options.TAGREQ:  
        if (options.TAGREQ in conf.PRODUCTS[args[0]] == False):
           parser.error(use)
        else:
           conf.TAGREQ.add(options.TAGREQ)
     else:
        conf.TAGREQ.add(['ALL'])
     
     #INITIALIZATION
     conf.LOGFILE=options.OutFilename
     conf.logger_setup()
     conf.logger=logging.getLogger('EMITestbed_PROCESSLOG')
     conf.logger.info('++++++++++++++++++++++++++++++++++++++++++++++++++')
     conf.logger.info('Starting the test for product:' + conf.PRODUCTREQ )
     conf.logger.info('Will execute tests matching TAG:' + str( conf.TAGREQ ))
     conf.loggerresults_setup()
     conf.loggerresults=logging.getLogger('EMITestbed_RESULTLOG')
     conf.loggerresults.info('++++++++++++++++++++++++++++++++++++++++++++++++++')
     conf.loggerresults.info('Starting the test for product:' + conf.PRODUCTREQ )
     conf.loggerresults.info('Test started at: ' + conf.STARTTIME)
     conf.loggerresults.info('Will execute tests matching TAG:' + str(conf.TAGREQ ))

     try:
        module = __import__(conf.PRODUCTREQ + '_class')
        class_ = getattr(module,conf.PRODUCTREQ)
        testclass = class_(conf)
     except Exception,e:
        conf.logger.error('Unable to instantiate testclass for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        sys.exit(-1)

     #CHECK PROXY EXISTENCE
     if conf.check_proxy()!=0: 
        print 'Could not find a valid proxy'
        sys.exit(-1)

     #CHECKING Testing ENV
     try:
        conf.logger.info('Checking testing environment')
        testclass.ckeck_environment(conf) 
     except Exception,e:
        conf.logger.error('Testing environment check fails for considered product test: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        conf.logger.error('Please control global configuration information and testbed status')
        sys.exit(-1)

     #RUNNING TEST   
     try:
        conf.logger.info('Running test')       
        testclass.run_test(conf) 
     except Exception,e:
        conf.logger.error('Unable to run test for considered product: '  + conf.PRODUCTREQ + '\t Excepion:' + str(e) )
        sys.exit(-1)

     conf.ENDTIME=time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
     conf.logger.info('Test completed at: ' + conf.ENDTIME)
     conf.loggerresults.info('Test completed at: ' + conf.ENDTIME)
     conf.logger.info('++++++++++++++++++++++++++++++++++++++++++++++++++')
