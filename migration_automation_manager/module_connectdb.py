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
import mysql.connector


class ModuleConnectDB:

    def __init__(self, module_log, module_configuration):
        """
        Define values for connection with database.
        :param moduleLog: Instance of the log class
        :type moduleLog: object
        """
        self.module_configuration = module_configuration
        self._log = module_log
        self._ip_db = self.module_configuration.ip_db
        self._user_db = self.module_configuration.user_db
        self._pass_db = self.module_configuration.pass_db
        self._database = self.module_configuration.database
        self._connection = None

    @property
    def connection(self):
        """
        Realize the connection with database.
        :return: Object of the connection on success, False on failure
        :rtype: object or bool
        """
        try:
            # create object with connection in database
            self._connection = mysql.connector.connect(host=self._ip_db, user=self._user_db, password=self._pass_db,
                                                       database=self._database)
            # return a object of connection in database
            return self._connection

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False
