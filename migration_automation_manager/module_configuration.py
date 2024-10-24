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
import configparser


class ModuleConfiguration:

    def __init__(self, development=None):
        self.development = development
        self.environment_config = None
        self.environment_log = None
        self.production = None
        self._configuration = None
        self._configuration_file = None
        self.queue = None

    def initialize(self):
        """
        Define name of the configuration file and read file.
        :return: False on failure
        :rtype: bool
        """
        try:
            if self.development is True:
                self.environment_config = "config_dev"
                self.environment_log = "logger"
                self.production = False
            else:
                self.environment_config = "config"
                self.environment_log = "logger"
                self.production = True
            # create instance of ConfigParser
            self._configuration = configparser.ConfigParser()
            # path of the configuration file
            self._configuration_file = "/opt/migration/files/migration.conf"
            # load configuration file
            self._configuration.read(self._configuration_file)
            return True

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_level(self):
        """
        Get log level in configuration file.
        :return: Value log level on success, False on failure
        :rtype: int or bool
        """
        try:
            # check string of log level configured and return ID corresponding to the level
            if str(self._configuration.get(self.environment_log, "loglevel")) == "logging.CRITICAL":
                # 50 is critical level
                return 50
            elif str(self._configuration.get(self.environment_log, "loglevel")) == "logging.ERROR":
                # 40 is error level
                return 40
            elif str(self._configuration.get(self.environment_log, "loglevel")) == "logging.WARNING":
                # 30 is warning level
                return 30
            elif str(self._configuration.get(self.environment_log, "loglevel")) == "logging.INFO":
                # 20 is info level
                return 20
            elif str(self._configuration.get(self.environment_log, "loglevel")) == "logging.DEBUG":
                # 10 is debug level
                return 10
            else:
                # default value for log level
                return 40

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filecheck_end(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilecheckend")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filemanager(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilemanager")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filezencheck(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilezencheck")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filedbcheck(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfiledbcheck")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filecpanel(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilecpanel")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filersync(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilersync")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filecheck(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilecheck")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filehandleaccount(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilehandleaccount")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filehandlephp(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilehandlephp")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filehandledns(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilehandledns")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_filecompare(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfilecompare")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def log_fileretry(self):
        """
        Get log file in configuration file.
        :return: Log file on success, False on failure
        :rtype: string or bool
        """
        try:
            # return o path of the log file
            return self._configuration.get(self.environment_log, "logfileretry")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def ip_db(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "ipdb")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def user_db(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "userdb")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def pass_db(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "passdb")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def database(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "database")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def token(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "token")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def token_es(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "tokenes")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def token_whmcs(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "whmcschangeserver")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def domain(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "domain")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def domain_es(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "domaines")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def user_queue(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "userqueue")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def password_queue(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "passwordqueue")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def host_queue(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "hostqueue")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def port_queue(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "portqueue")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    def key(self, queue):
        """
        """
        try:
            self.queue = queue
            if self.queue == "rsync":
                return self._configuration.get(self.environment_config, "keyrsync")
            elif self.queue == "rsync_last":
                return self._configuration.get(self.environment_config, "keyrsynclast")
            elif self.queue == "cpanel":
                return self._configuration.get(self.environment_config, "keycpanel")
            elif self.queue == "check":
                return self._configuration.get(self.environment_config, "keycheck")
            elif self.queue == "check_end":
                return self._configuration.get(self.environment_config, "keycheckend")
            elif self.queue == "manager":
                return self._configuration.get(self.environment_config, "keymanager")
            elif self.queue == "compare":
                return self._configuration.get(self.environment_config, "keycompare")
            elif self.queue == "handle_php":
                return self._configuration.get(self.environment_config, "keyhandlephp")
            elif self.queue == "handle_dns":
                return self._configuration.get(self.environment_config, "keyhandledns")
            elif self.queue == "handle_account":
                return self._configuration.get(self.environment_config, "keyhandleaccount")
            else:
                return False

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def report_dir(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "reportdir")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def playbook_account(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "playbookaccount")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def playbook_dns(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "playbookdns")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def playbook_php(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "playbookphp")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def playbook_check(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "playbookcheck")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def playbook_cpanel(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "playbookcpanel")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def playbook_rsync(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "playbookrsync")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def private_keypath(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "privatekeypath")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def private_keypath_all(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "privatekeypathall")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False

    @property
    def ansible_roles(self):
        """
        """
        try:
            return self._configuration.get(self.environment_config, "ansibleroles")

        except Exception as er:
            # only print the error, since moduleLog there isn't instance in ModuleConfiguration class
            print("{} - {}".format(self.__class__.__name__, er))
            return False
