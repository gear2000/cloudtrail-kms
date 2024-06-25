#!/usr/bin/env python

import os
import logging

class SimpleLogger(object):

    def __init__(self,name):
        """
        Initializes a SimpleLogger object with the given name and optional keyword arguments.

        Parameters:
            name (str): The name of the logger.

        Returns:
            None

        Description:
            This function initializes a SimpleLogger object with the given name. It sets the log level to DEBUG and creates a file handler that logs even debug messages. The log directory is set to "/tmp/log" and the log file is named "main.log". The file handler is added to the logger with the specified formatter. The logger and file handler are stored as attributes of the SimpleLogger object.
            The class attribute self.direct is the direct logger whereas the self.info/debug/warn/error/critical methods are used to log messages with some emphasis

        Note:
            The os.system() function is used to create the log directory if it does not exist.
        """

        self.classname = 'SimpleLogger'

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        logdir = "/tmp/log"
        
        if not os.path.exists(logdir):
            os.system("mkdir -p {}".format(logdir))

        logfile = "{}/{}".format(logdir,"main.log")

        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        self.direct = logger
        self.aggregate_msg = None

    def info(self,message):
        """
        Logs an informational message using the logger.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """
        self.direct.info(message)

    def debug(self,message):
        """
        Logs an informational message using the logger.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """
        self.direct.debug(message)

    def critical(self,message):
        """
        Logs a critical message using the logger and encloses with "!" for emphasis

        Parameters:
            message (str): The critical message to be logged.
            
        Returns:
            None
        """

        self.direct.critical("!"*32)
        self.direct.critical(message)
        self.direct.critical("!"*32)

    def error(self,message):
        """
        Logs an error message using the logger, surrounding it with "*" for emphasis.

        Parameters:
            message (str): The error message to be logged.

        Returns:
            None
        """
        
        self.direct.error("*"*32)
        self.direct.error(message)
        self.direct.error("*"*32)

    def warn(self,message):
        """
        Logs an error message using the logger, surrounding it with "-" for emphasis.

        Args:
            message (str): The warning message to be logged.

        Returns:
            None
        """

        self.direct.warning("-"*32)
        self.direct.warning(message)
        self.direct.warning("-"*32)