# -*- coding: utf-8 -*-
"""


- Contributors
Elliann Marks <elian.markes@gmail.com>





**- Version 1.0 - 18/09/2019**
**Functions - main**
**Libraries - ModuleMain and time**
**Dependencies - no**
**Parameters - no**

"""

# libraries
import logging
from contextlib import closing
from datetime import datetime


class ModuleLog:

    def __init__(self, module_configuration, daemon):
        """
        Define values for create log instance
        :param module_configuration:  Instance of the moduleConfiguration class
        :type module_configuration: object
        """
        self.module_configuration = module_configuration
        self.daemon = daemon
        # configuration logging
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.log_file = None
        self.log_handler = None
        self.log_level = None
        self.log = None
        self.log_formatter = None

    def initialize(self):
        try:
            if self.daemon == 1:
                self.log_file = str(self.module_configuration.log_filezencheck) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 2:
                self.log_file = str(self.module_configuration.log_filecpanel) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 3:
                self.log_file = str(self.module_configuration.log_filersync) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 5:
                self.log_file = str(self.module_configuration.log_filecheck) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 6:
                self.log_file = str(self.module_configuration.log_filemanager) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 7:
                self.log_file = str(self.module_configuration.log_filecheck_end) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 8:
                self.log_file = str(self.module_configuration.log_filecompare) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 9:
                self.log_file = str(self.module_configuration.log_filehandlephp) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 10:
                self.log_file = str(self.module_configuration.log_filehandledns) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 11:
                self.log_file = str(self.module_configuration.log_filehandleaccount) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 13:
                self.log_file = str(self.module_configuration.log_fileretry) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            elif self.daemon == 14:
                self.log_file = str(self.module_configuration.log_filedbcheck) + "_" + str(
                    datetime.now().strftime('%d_%m_%Y')) + ".log"
            self.log_level = self.module_configuration.log_level
            # configuration log
            self.log = logging.getLogger(__name__)
            self.log.setLevel(self.log_level)
            with closing(logging.FileHandler(self.log_file)) as self.log_handler:
                self.log_handler.setLevel(self.log_level)
                self.log_formatter = logging.Formatter(self.log_format)
                self.log_handler.setFormatter(self.log_formatter)
                self.log.addHandler(self.log_handler)
            return True

        except Exception as er:
            print("{} - {}".format(self.__class__.__name__, er))
            return False
