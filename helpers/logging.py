import datetime
import inspect
import logging


# from io import StringIO
from framework.configuration import TestRun


class Logger():
    current_log_file = ''
    displayDebugLevel = 99

    @staticmethod
    def logging_setup(test_method):

        # logging.debug("a debug message")
        # logging.info("an info message")
        # logging.warning("a warning message")
        # logging.error("an error message")
        # logging.critical("a critical message")
        # logging.log(0, "a 'log' level 0 message")
        # #logging.exception("an exception message")
        log = test_method + '_' + str(
            datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        if Logger.current_log_file == '':
            logging.shutdown()
            root_logger = logging.getLogger()

            for _ in list(root_logger.handlers):
                root_logger.removeHandler(_)
                _.flush()
                _.close()
            for _ in list(root_logger.filters):
                root_logger.removeFilter(_)
                _.flush()
                _.close()

            logFileName = TestRun.log_file_base_path + log + '.log'
            # logFormat = "%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p"
            logFormat = "%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%y/%m/%d %I:%M:%S %p"

            # logging.getLogger(logFileName).__format__()
            logging.basicConfig(filename=logFileName, level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p')
            Logger.log_and_debug(5, "info", "***** Starting Script: " + log + " *****")
            Logger.log_and_debug(5, "info", "Log file is: " + logFileName)  # + "; Line format is: " + logFormat)

            Logger.current_log_file = logFileName
            return log, logFileName
        return log, Logger.current_log_file

    @staticmethod
    def log_and_debug(debugLevel, logLevel, debugMesssage):
        #### On-screen Display of Debug Messages
        ####
        # debugLevel is a numeric value. 
        #   Values are: 0-5 and 99, in increasing importance. 
        #   99 means always print this message. This is good for the order number confirmation and such. 


            # I researched this method of getting values, but it seems longer even though it uses variable names while the other uses indexes. 
            # def get_calling_script_name():
                # frm = inspect.stack()[1]
                # mod = inspect.getmodule(frm[0])
                # print '[%s] %s' % (mod.__name__, msg)
                # frame = inspect.stack()[1]
                # module = inspect.getmodule(frame[0])
                # filename = module.__file__


        callStack = inspect.stack()
        callLevel0 = callStack[0][3] + "[" + str(callStack[0][2]) + "]"
        callLevel1 = callStack[1][3] + "[" + str(callStack[1][2]) + "]"
        callLevel2 = callStack[2][3] + "[" + str(callStack[2][2]) + "]"
        # callLevel3 = callStack[3][3] + "[" + str(callStack[2][2]) + "]"
  
        ### Separate level 99 messages so they stand out from other messages
        # if debugLevel >= OP.displayDebugLevel:  print("{0:12} - {1:40} - {2:200}".format(U.actualServer, callLevel2, debugMesssage))
        # if debugLevel >= OP.displayDebugLevel:  print( callLevel1 + " - " + callLevel2 + " - " + callLevel3 + ": " + debugMesssage)
        if debugLevel == 99: print("*"*120 + "\n")
        
        
        
        #### Logging Messages to a Log File
        ####
        
        # logLevel is a text value and corresponds to python and log4j log levels - except logLevel 0, which means don't log this message. 

        # logging.debug("a debug message")
        # logging.info("an info message")
        # logging.warning("a warning message")
        # logging.error("an error message")
        # logging.critical("a critical message")
        # logging.log(0, "a 'log' level 0 message")
        # #logging.exception("an exception message")

        if   logLevel == '0':         pass 
        elif logLevel == 'debug':
            print(debugMesssage)
            logging.debug(callLevel0 + " - " + callLevel1 + " - " + callLevel3 + ": " + debugMesssage)
        elif logLevel == 'info':
            print(debugMesssage)
            logging.info(callLevel0 + " - " + callLevel1 + " - " + callLevel2 + ": " + debugMesssage)
        elif logLevel == 'warning':
            print(debugMesssage)
            logging.warning(callLevel0 + " - " + callLevel1 + " - " + callLevel2 + ": " + debugMesssage)
        elif logLevel == 'error':
            print(debugMesssage)
            logging.error( callLevel0 + " - " + callLevel1 + " - " + callLevel2 + ": " + debugMesssage)
        elif logLevel == 'critical':
            print(debugMesssage)
            logging.info(callLevel0 + " - " + callLevel1 + " - " + callLevel2 + ": " + debugMesssage)
        elif logLevel == 'log':
            print(debugMesssage)
            logging.info(callLevel0 + " - " + callLevel1 + " - " + callLevel2 + ": " + debugMesssage)
        elif logLevel == 'exception':
            print(debugMesssage)
            logging.info(callLevel0 + " - " + callLevel1 + " - " + callLevel2 + ": " + debugMesssage)

                
    
    @staticmethod
    def log_exception(e):  Logger.log_and_debug(99, "exception", 'Exception error: '+ str(e))
