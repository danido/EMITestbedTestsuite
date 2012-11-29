EMITestbedTestsuite
===================

Simple Testsuite to run basic integration tests across EMI products

FileStructure:
├── EMITestbed.py  		----> MAIN Function
├── JDL				----> JDL Files directory
│   ├── basictest.jdl     	----> JDL for a basictest
│   └── mpitest.jdl
├── LIB
│   ├── common_conf.py		----> Common configuration library
│   └── LFC_class.py		----> CLass implementing a test for a given product
|── OUT                         ----> Outfiles are stored in this directory
├── README.md
└── testscript.txt		----> Python shell commands for a quick test.


-----------------------------------------------------------------------------------
├── EMITestbed.py               ----> MAIN Function

USAGE $> python EMITestbed.py [-t TAGDEFINEDFORPRODUCT] LFC
-> Only one product per program execution.
After some setup and checks, it instantiates the requested Product class and runs the two methods defined in each Product class: testclass.run()  and testclass.check_results()

It has two logfiles, handled by logging python module: 
1) DATE_PROCESS.log  ---->   All details about testsuite run process are stored here
2) DATE_RESULTS.log  ---->   Just test name and test results are stored here


-----------------------------------------------------------------------------------
├── LIB/common_conf.py          ----> Common configuration

ALL commob configuration info and methods are in this class, in particular:
- DICTIONARY->PRODUCTS  = Stores Products for which a class test with relative TESTTAGS has been defined
- DICTIONARY->CONFFILES = List of files used in the testsuite
- DICTIONARY->TESTBED   =  Structured dictionary describing the available testbed: PRODUCTS|RESOURCES|RESOURCES_CONF
- DICTIONARY->.UTILS_CLI = Structured dictionary implementing parametrized CLI per product
- OPERATIONS GLOBAL VARIABLES : ID, NUM_STATUS_RETRIEVALS, SLEEP_TIME....
- METHOD: Logging setup: logger_setup, loggerresults_setup
- METHOD: run_command, runs a generic command passed in args
- METHOD: run_command_until, runs a generic command until condition
- METHOD: jobsubmit
- METHOD: waitjobuntilterminalstatus
- METHOD......

-----------------------------------------------------------------------------------
│── LIB/LFC_class.py            ----> CLass implementing a test for a given product

Sample class implementing a test for LFC. You can use it as a template.
Args: takes common_conf class with global configuration 
Requirements: 
- module name should be in the format PRODUCTNAME_class.py  with PRODUCTNAME(conf): class defined in it
- run_test()          method must be implemented (running the test and returning 0: OK | -1 process errors | + N test fails ) 
- check_environment() method must be implemented (checks that testbed is properly configured and in good shape)
