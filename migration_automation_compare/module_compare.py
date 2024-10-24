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
from migration_automation_manager.module_database import ModuleDatabase
from migration_automation_manager.module_publish import ModulePublish
import os
import json
import ast
from contextlib import closing


class ModuleCompare:

    def __init__(self, module_log, module_configuration):
        """
        Responsible for execute the checking playbooks and store result in dict.
        :param module_log: log instance
        :type module_log: Object
        """
        try:
            self._log = module_log
            self.module_configuration = module_configuration
            self.general_error = False
            # create the instances
            self.module_database = ModuleDatabase(self._log, self.module_configuration)
            # get values collected
            self.values_ticket = None
            self.main_domain = None
            self.ticket_id = None
            self.thread_id = None
            self.values_database = None
            self.request_type = None
            self.report_dir = self.module_configuration.report_dir
            self.set_domain = None
            self.set_value_php = None
            self.set_variable_php = None
            self.set_version_php = None
            self.domain = None
            self.domain_end = None
            self.addon_domains = None
            self.parked_domains = None
            self.sub_domains = None
            self.addon_domains_end = None
            self.parked_domains_end = None
            self.sub_domains_end = None
            self.addon_domain = None
            self.parked_domain = None
            self.sub_domain = None
            self.addon_domain_end = None
            self.parked_domain_end = None
            self.sub_domain_end = None
            self.report_casepath = None
            self.file_list_domains = None
            self.result_list_domains = None
            self.open_list_domains = None
            self.file_list_domains_end = None
            self.result_list_domains_end = None
            self.open_list_domains_end = None
            self.file_list_popsdisk = None
            self.result_list_popsdisk = None
            self.open_list_popsdisk = None
            self.file_list_popsdisk_end = None
            self.result_list_popsdisk_end = None
            self.open_list_popsdisk_end = None
            self.len_mysql_databases = None
            self.len_mysql_databases_end = None
            self.len_popsdisk = None
            self.len_popsdisk_end = None
            self.file_mysql_databases = None
            self.open_mysql_databases = None
            self.result_mysql_databases = None
            self.file_mysql_databases_end = None
            self.open_mysql_databases_end = None
            self.result_mysql_databases_end = None
            self.file_phpinfo = None
            self.open_phpinfo = None
            self.result_phpinfo = None
            self.file_phpinfo_end = None
            self.open_phpinfo_end = None
            self.result_phpinfo_end = None
            self.php_version = None
            self.allow_url_fopen = None
            self.max_input_vars = None
            self.max_execution_time = None
            self.memory_limit = None
            self.post_max_size = None
            self.upload_max_filesize = None
            self.php_version_end = None
            self.allow_url_fopen_end = None
            self.max_input_vars_end = None
            self.max_execution_time_end = None
            self.memory_limit_end = None
            self.post_max_size_end = None
            self.upload_max_filesize_end = None
            self.mysql_version_src = None
            self.mysql_version_dst = None
            self.file_mysql_version_src = None
            self.file_mysql_version_dst = None
            self.open_mysql_version_src = None
            self.open_mysql_version_dst = None
            self.result_mysql_version_src = None
            self.result_mysql_version_dst = None
            self.checking_mysql = None
            self.message = None
            self.queue_manager = ModulePublish(self._log, "manager", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                               self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("manager"))
            self.queue_handle_php = ModulePublish(self._log, "handle_php", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                                  self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("handle_php"))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            self.general_error = True

    def initialize(self, values_ticket):
        try:
            # get values collected
            self.domain = None
            self.domain_end = None
            self.php_version = None
            self.allow_url_fopen = None
            self.max_input_vars = None
            self.max_execution_time = None
            self.memory_limit = None
            self.post_max_size = None
            self.upload_max_filesize = None
            self.php_version_end = None
            self.allow_url_fopen_end = None
            self.max_input_vars_end = None
            self.max_execution_time_end = None
            self.memory_limit_end = None
            self.post_max_size_end = None
            self.upload_max_filesize_end = None
            self.file_phpinfo = None
            self.open_phpinfo = None
            self.result_phpinfo = None
            self.file_phpinfo_end = None
            self.open_phpinfo_end = None
            self.result_phpinfo_end = None
            self.file_list_domains = None
            self.result_list_domains = None
            self.open_list_domains = None
            self.file_list_domains_end = None
            self.result_list_domains_end = None
            self.open_list_domains_end = None
            self.file_list_popsdisk = None
            self.result_list_popsdisk = None
            self.open_list_popsdisk = None
            self.file_list_popsdisk_end = None
            self.result_list_popsdisk_end = None
            self.open_list_popsdisk_end = None
            self.mysql_version_src = None
            self.mysql_version_dst = None
            self.file_mysql_version_src = None
            self.file_mysql_version_dst = None
            self.open_mysql_version_src = None
            self.open_mysql_version_dst = None
            self.result_mysql_version_src = None
            self.result_mysql_version_dst = None
            self.checking_mysql = None
            self.len_popsdisk = None
            self.len_popsdisk_end = None
            self.report_casepath = None
            self.addon_domains = None
            self.parked_domains = None
            self.sub_domains = None
            self.addon_domains_end = None
            self.parked_domains_end = None
            self.sub_domains_end = None
            self.values_ticket = None
            self.main_domain = None
            self.request_type = None
            self.ticket_id = None
            self.thread_id = None
            self.values_database = None
            self.general_error = False
            # get values collected
            self.values_ticket = values_ticket
            self.ticket_id = self.values_ticket.get('id')
            self.thread_id = self.values_ticket.get('thread_id')
            # get values in database
            if self.ticket_id is not None and self.ticket_id is not False and \
                    self.thread_id is not None and self.thread_id is not False:
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "compare")
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 2:
                    self.main_domain = self.values_database[0]
                    self.request_type = self.values_database[1]
                    return True
                else:
                    self.general_error = True
                    self._log.error("Failed compare get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed compare get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize compare - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                self.module_database.update_analyzing("compare", 1, self.thread_id)
                self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                self.handle_list_domains()
                self.handle_list_popsdisk()
                self.handle_mysql_databases()
                if len(self.sub_domains) > 0:
                    self.handle_phpinfo_subdomains()
                if len(self.addon_domains) > 0:
                    self.handle_phpinfo_addondomains()
                if len(self.parked_domains) > 0:
                    self.handle_phpinfo_parkeddomains()
                self.handle_phpinfo_maindomain()
                if self.general_error is False:
                    if self.len_mysql_databases == self.len_mysql_databases_end and \
                            self.len_popsdisk == self.len_popsdisk_end and \
                            len(self.addon_domains) == len(self.addon_domains_end) and \
                            len(self.parked_domains) == len(self.parked_domains_end) and \
                            len(self.sub_domains) == len(self.sub_domains_end):
                        self.module_database.update_analyzing("compare", 3, self.thread_id)
                        if self.message_manager():
                            self._log.info("Send manager {}".format(self.message))
                        else:
                            self._log.info("Failed send manager {}".format(self.message))
                    else:
                        self._log.info("Failed in compare values between source and destination - {}".format(self.values_ticket))
                        self.module_database.update_analyzing("compare", 2, self.thread_id)
                        if self.message_manager():
                            self._log.info("Send manager {}".format(self.message))
                        else:
                            self._log.info("Failed send manager {}".format(self.message))
                else:
                    self._log.debug("General error true after get values of the source and destination - {}".format(self.values_ticket))
                    self.module_database.update_analyzing("compare", 2, self.thread_id)
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
            else:
                # critical log
                self._log.critical("Error compare - generalError {} - values {}".format(self.general_error, self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("process compare - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_manager(self):
        try:
            self.message = dict()
            self.message.update({'sender': 'compare'})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            if self.mysql_version_dst is not False and self.mysql_version_dst is not None and \
                    self.mysql_version_src is not False and self.mysql_version_src is not None and \
                    self.checking_mysql is not None:
                self.message.update({'checking_mysql': self.checking_mysql})
                self.message.update({'mysql_version_src': self.mysql_version_src})
                self.message.update({'mysql_version_dst': self.mysql_version_dst})
            self.queue_manager.publish(self.message)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message compare - {} - {}".format(self.__class__.__name__, er))
            return False

    def mysql_version(self):
        try:
            self.file_mysql_version_src = os.path.join(self.report_casepath, "source/mysqlServerVersion.json")
            self.file_mysql_version_dst = os.path.join(self.report_casepath, "destination/mysqlServerVersion.json")
            if os.path.exists(self.file_mysql_version_src) and os.path.exists(self.file_mysql_version_dst):
                try:
                    with closing(open(self.file_mysql_version_src)) as self.open_mysql_version_src:
                        self.result_mysql_version_src = json.load(self.open_mysql_version_src)
                        if int(self.result_mysql_version_src['metadata']['result']) == 1:
                            self.mysql_version_src = self.result_mysql_version_src['data']['version'].split(".")
                            if len(self.mysql_version_src) >= 2:
                                self.mysql_version_src = ".".join(self.mysql_version_src[:2])
                            elif len(self.mysql_version_src) == 1:
                                self.mysql_version_src = self.mysql_version_src
                            else:
                                self.mysql_version_src = False
                        else:
                            self.mysql_version_src = False

                    with closing(open(self.file_mysql_version_dst)) as self.open_mysql_version_dst:
                        self.result_mysql_version_dst = json.load(self.open_mysql_version_dst)
                        if int(self.result_mysql_version_dst['metadata']['result']) == 1:
                            self.mysql_version_dst = self.result_mysql_version_dst['data']['version'].split(".")
                            if len(self.mysql_version_dst) >= 2:
                                self.mysql_version_dst = ".".join(self.mysql_version_dst[:2])
                            elif len(self.mysql_version_dst) == 1:
                                self.mysql_version_dst = self.mysql_version_dst
                            else:
                                self.mysql_version_dst = False
                        else:
                            self.mysql_version_dst = False

                    if self.mysql_version_src is not False and self.mysql_version_src is not None and \
                            self.mysql_version_dst is not False and self.mysql_version_dst is not None:
                        if float(self.mysql_version_src) >= 5.6 and float(self.mysql_version_dst) >= 5.6:
                            self.checking_mysql = False
                        else:
                            self.checking_mysql = True

                except Exception as er:
                    self.mysql_version_src = False
                    self.mysql_version_dst = False
                    self.checking_mysql = False
                    self._log.error("Failed get mysql version src or dst in json - {}".format(self.values_ticket, er))
                    return False
            else:
                self.mysql_version_src = False
                self.mysql_version_dst = False
                self.checking_mysql = False
                self._log.error("mysqlServerVersion.json not found in src or dst - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("mysql_version - {} - {}".format(self.__class__.__name__, er))
            return False

    def handle_list_domains(self):
        try:
            self.file_list_domains = os.path.join(self.report_casepath, "source/listDomains.json")
            self.file_list_domains_end = os.path.join(self.report_casepath, "destination_end/listDomains.json")
            if os.path.exists(self.file_list_domains) and os.path.exists(self.file_list_domains_end):
                try:
                    with closing(open(self.file_list_domains)) as self.open_list_domains:
                        self.result_list_domains = json.load(self.open_list_domains)
                        if int(self.result_list_domains['result']['status']) == 1 and self.result_list_domains['result']['errors'] is None:
                            self.addon_domains = self.result_list_domains['result']['data']['addon_domains']
                            self.parked_domains = self.result_list_domains['result']['data']['parked_domains']
                            self.sub_domains = self.result_list_domains['result']['data']['sub_domains']
                            self.domain = self.result_list_domains['result']['data']['main_domain']
                        else:
                            self._log.error("Failed get data in listDomains.json - {}".format(self.values_ticket))
                            self.general_error = True

                    with closing(open(self.file_list_domains_end)) as self.open_list_domains_end:
                        self.result_list_domains_end = json.load(self.open_list_domains_end)
                        if int(self.result_list_domains_end['result']['status']) == 1 and self.result_list_domains_end['result']['errors'] is None:
                            self.addon_domains_end = self.result_list_domains_end['result']['data']['addon_domains']
                            self.parked_domains_end = self.result_list_domains_end['result']['data']['parked_domains']
                            self.sub_domains_end = self.result_list_domains_end['result']['data']['sub_domains']
                            self.domain_end = self.result_list_domains['result']['data']['main_domain']
                        else:
                            self._log.error("Failed get data end in listDomains.json - {}".format(self.values_ticket))
                            self.general_error = True

                except Exception as er:
                    self.general_error = True
                    self._log.error("Failed handled listDomains.json - {} - {}".format(self.values_ticket, er))
                    return False
            else:
                self.general_error = True
                self._log.error("listDomains.json not found - {}".format(self.values_ticket))
                return False

        except Exception as er:
            self.general_error = True
            # generate a error log
            self._log.error("list_domains in compare - {} - {}".format(self.__class__.__name__, er))
            return False

    def handle_list_popsdisk(self):
        try:
            self.file_list_popsdisk = os.path.join(self.report_casepath, "source/listPopsDisk.json")
            self.file_list_popsdisk_end = os.path.join(self.report_casepath, "destination_end/listPopsDisk.json")
            if os.path.exists(self.file_list_popsdisk) and os.path.exists(self.file_list_popsdisk_end):
                try:
                    with closing(open(self.file_list_popsdisk)) as self.open_list_popsdisk:
                        self.result_list_popsdisk = json.load(self.open_list_popsdisk)
                        if int(self.result_list_popsdisk['result']['status']) == 1 and self.result_list_popsdisk['result']['errors'] is None:
                            self.len_popsdisk = len(self.result_list_popsdisk['result']['data'])
                        else:
                            self._log.error("Failed get data in listPopsDisk.json - {}".format(self.values_ticket))
                            self.general_error = True

                    with closing(open(self.file_list_popsdisk_end)) as self.open_list_popsdisk_end:
                        self.result_list_popsdisk_end = json.load(self.open_list_popsdisk_end)
                        if int(self.result_list_popsdisk_end['result']['status']) == 1 and self.result_list_popsdisk_end['result']['errors'] is None:
                            self.len_popsdisk_end = len(self.result_list_popsdisk['result']['data'])
                        else:
                            self._log.error("Failed get data end in listPopsDisk.json - {}".format(self.values_ticket))
                            self.general_error = True

                except Exception as er:
                    self.general_error = True
                    self._log.error("Failed handled listPopsDisk.json - {} - {}".format(self.values_ticket, er))
                    return False
            else:
                self.general_error = True
                self._log.error("listPopsDisk.json not found - {}".format(self.values_ticket))
                return False

        except Exception as er:
            self.general_error = True
            # generate a error log
            self._log.error("list_popsdisk in compare - {} - {}".format(self.__class__.__name__, er))
            return False

    def handle_mysql_databases(self):
        try:
            self.file_mysql_databases = os.path.join(self.report_casepath, "source/mysqlDatabases.json")
            self.file_mysql_databases_end = os.path.join(self.report_casepath, "destination_end/mysqlDatabases.json")
            if os.path.exists(self.file_mysql_databases) and os.path.exists(self.file_mysql_databases_end):
                try:
                    with closing(open(self.file_mysql_databases)) as self.open_mysql_databases:
                        self.result_mysql_databases = json.load(self.open_mysql_databases)
                        if int(self.result_mysql_databases['metadata']['result']) == 1 and self.result_mysql_databases['metadata']['reason'] == "OK":
                            self.len_mysql_databases = len(self.result_mysql_databases['data']['mysql_databases'].keys())
                        else:
                            self._log.error("Failed get data in mysqlDatabases.json - {}".format(self.values_ticket))
                            self.general_error = True

                    with closing(open(self.file_mysql_databases_end)) as self.open_mysql_databases_end:
                        self.result_mysql_databases_end = json.load(self.open_mysql_databases_end)
                        if int(self.result_mysql_databases_end['metadata']['result']) == 1 and self.result_mysql_databases_end['metadata']['reason'] == "OK":
                            self.len_mysql_databases_end = len(self.result_mysql_databases['data']['mysql_databases'].keys())
                        else:
                            self._log.error("Failed get data end in mysqlDatabases.json - {}".format(self.values_ticket))
                            self.general_error = True

                except Exception as er:
                    self.general_error = True
                    self._log.error("Failed handled mysqlDatabases.json - {} - {}".format(self.values_ticket, er))
                    return False
            else:
                self.general_error = True
                self._log.error("mysqlDatabases.json not found - {}".format(self.values_ticket))
                return False

        except Exception as er:
            self.general_error = True
            # generate a error log
            self._log.error("mysql_databases in compare - {} - {}".format(self.__class__.__name__, er))
            return False

    def handle_phpinfo_maindomain(self):
        try:
            self.php_version = None
            self.allow_url_fopen = None
            self.max_input_vars = None
            self.max_execution_time = None
            self.memory_limit = None
            self.post_max_size = None
            self.upload_max_filesize = None
            self.php_version_end = None
            self.allow_url_fopen_end = None
            self.max_input_vars_end = None
            self.max_execution_time_end = None
            self.memory_limit_end = None
            self.post_max_size_end = None
            self.upload_max_filesize_end = None
            self.file_phpinfo = None
            self.file_phpinfo_end = None
            self.open_phpinfo = None
            self.open_phpinfo_end = None
            self.result_phpinfo = None
            self.result_phpinfo_end = None
            self.file_phpinfo = os.path.join(self.report_casepath, "source/" + self.main_domain + ".json")
            self.file_phpinfo_end = os.path.join(self.report_casepath, "destination_end/" + self.main_domain + ".json")
            if os.path.exists(self.file_phpinfo) and os.path.exists(self.file_phpinfo_end):
                with closing(open(self.file_phpinfo)) as self.open_phpinfo:
                    self.result_phpinfo = ast.literal_eval(json.load(self.open_phpinfo))
                    self.php_version = "".join(self.result_phpinfo['Core']['PHP Version'].split(".")[:2])
                    self.allow_url_fopen = self.result_phpinfo['Core']['allow_url_fopen']
                    self.max_input_vars = self.result_phpinfo['Core']['max_input_vars']
                    self.max_execution_time = self.result_phpinfo['Core']['max_execution_time']
                    self.memory_limit = self.result_phpinfo['Core']['memory_limit']
                    self.post_max_size = self.result_phpinfo['Core']['post_max_size']
                    self.upload_max_filesize = self.result_phpinfo['Core']['upload_max_filesize']

                with closing(open(self.file_phpinfo_end)) as self.open_phpinfo_end:
                    self.result_phpinfo_end = ast.literal_eval(json.load(self.open_phpinfo_end))
                    self.php_version_end = "".join(self.result_phpinfo_end['Core']['PHP Version'].split(".")[:2])
                    self.allow_url_fopen_end = self.result_phpinfo_end['Core']['allow_url_fopen']
                    self.max_input_vars_end = self.result_phpinfo_end['Core']['max_input_vars']
                    self.max_execution_time_end = self.result_phpinfo_end['Core']['max_execution_time']
                    self.memory_limit_end = self.result_phpinfo_end['Core']['memory_limit']
                    self.post_max_size_end = self.result_phpinfo_end['Core']['post_max_size']
                    self.upload_max_filesize_end = self.result_phpinfo_end['Core']['upload_max_filesize']

                if self.php_version != self.php_version_end:
                    if self.request_type == 1:
                        self._log.debug("phpversion in request_type turbo")
                        if int(self.php_version) < 70:
                            self.message_set_phpversion(self.main_domain, "70")
                        else:
                            self.message_set_phpversion(self.main_domain, self.php_version)
                    else:
                        self._log.debug("phpversion in request_type others")
                        self.message_set_phpversion(self.main_domain, self.php_version)
                if self.allow_url_fopen != self.allow_url_fopen_end:
                    self.message_set_phpini(self.main_domain, self.allow_url_fopen[0], "allow_url_fopen")
                if self.max_input_vars != self.max_input_vars_end:
                    self.message_set_phpini(self.main_domain, self.max_input_vars[0], "max_input_vars")
                if self.max_execution_time != self.max_execution_time_end:
                    self.message_set_phpini(self.main_domain, self.max_execution_time[0], "max_execution_time")
                if self.memory_limit != self.memory_limit_end:
                    self.message_set_phpini(self.main_domain, self.memory_limit[0], "memory_limit")
                if self.post_max_size != self.post_max_size_end:
                    self.message_set_phpini(self.main_domain, self.post_max_size[0], "post_max_size")
                if self.upload_max_filesize != self.upload_max_filesize_end:
                    self.message_set_phpini(self.main_domain, self.upload_max_filesize[0], "upload_max_filesize")

                self._log.debug("Source maindomain - {} - {}".format(self.main_domain, self.php_version))
                self._log.debug("Destination maindomain - {} - {}".format(self.main_domain, self.php_version_end))
            else:
                self._log.error("phpinfo maindomain not found - {} - {}".format(self.values_ticket, self.main_domain))

        except Exception as er:
            # generate a error log
            self._log.error("phpinfo maindomain - {} - {}".format(self.__class__.__name__, er))
            return False

    def handle_phpinfo_subdomains(self):
        try:
            for self.sub_domain in self.sub_domains:
                self.php_version = None
                self.allow_url_fopen = None
                self.max_input_vars = None
                self.max_execution_time = None
                self.memory_limit = None
                self.post_max_size = None
                self.upload_max_filesize = None
                self.php_version_end = None
                self.allow_url_fopen_end = None
                self.max_input_vars_end = None
                self.max_execution_time_end = None
                self.memory_limit_end = None
                self.post_max_size_end = None
                self.upload_max_filesize_end = None
                self.file_phpinfo = None
                self.file_phpinfo_end = None
                self.open_phpinfo = None
                self.open_phpinfo_end = None
                self.result_phpinfo = None
                self.result_phpinfo_end = None
                try:
                    for self.sub_domain_end in self.sub_domains_end:
                        if self.sub_domain == self.sub_domain_end:
                            self.file_phpinfo = os.path.join(self.report_casepath, "source/" + self.sub_domain + ".json")
                            self.file_phpinfo_end = os.path.join(self.report_casepath, "destination_end/" + self.sub_domain_end + ".json")
                            if os.path.exists(self.file_phpinfo) and os.path.exists(self.file_phpinfo_end):
                                with closing(open(self.file_phpinfo)) as self.open_phpinfo:
                                    self.result_phpinfo = ast.literal_eval(json.load(self.open_phpinfo))
                                    self.php_version = "".join(self.result_phpinfo['Core']['PHP Version'].split(".")[:2])
                                    self.allow_url_fopen = self.result_phpinfo['Core']['allow_url_fopen']
                                    self.max_input_vars = self.result_phpinfo['Core']['max_input_vars']
                                    self.max_execution_time = self.result_phpinfo['Core']['max_execution_time']
                                    self.memory_limit = self.result_phpinfo['Core']['memory_limit']
                                    self.post_max_size = self.result_phpinfo['Core']['post_max_size']
                                    self.upload_max_filesize = self.result_phpinfo['Core']['upload_max_filesize']

                                with closing(open(self.file_phpinfo_end)) as self.open_phpinfo_end:
                                    self.result_phpinfo_end = ast.literal_eval(json.load(self.open_phpinfo_end))
                                    self.php_version_end = "".join(self.result_phpinfo_end['Core']['PHP Version'].split(".")[:2])
                                    self.allow_url_fopen_end = self.result_phpinfo_end['Core']['allow_url_fopen']
                                    self.max_input_vars_end = self.result_phpinfo_end['Core']['max_input_vars']
                                    self.max_execution_time_end = self.result_phpinfo_end['Core']['max_execution_time']
                                    self.memory_limit_end = self.result_phpinfo_end['Core']['memory_limit']
                                    self.post_max_size_end = self.result_phpinfo_end['Core']['post_max_size']
                                    self.upload_max_filesize_end = self.result_phpinfo_end['Core']['upload_max_filesize']

                                if self.php_version != self.php_version_end:
                                    if self.request_type == 1:
                                        if int(self.php_version) < 70:
                                            self.message_set_phpversion(self.sub_domain_end, "70")
                                        else:
                                            self.message_set_phpversion(self.sub_domain_end, self.php_version)
                                    else:
                                        self.message_set_phpversion(self.sub_domain_end, self.php_version)
                                if self.allow_url_fopen != self.allow_url_fopen_end:
                                    self.message_set_phpini(self.sub_domain_end, self.allow_url_fopen[0], "allow_url_fopen")
                                if self.max_input_vars != self.max_input_vars_end:
                                    self.message_set_phpini(self.sub_domain_end, self.max_input_vars[0], "max_input_vars")
                                if self.max_execution_time != self.max_execution_time_end:
                                    self.message_set_phpini(self.sub_domain_end, self.max_execution_time[0], "max_execution_time")
                                if self.memory_limit != self.memory_limit_end:
                                    self.message_set_phpini(self.sub_domain_end, self.memory_limit[0], "memory_limit")
                                if self.post_max_size != self.post_max_size_end:
                                    self.message_set_phpini(self.sub_domain_end, self.post_max_size[0], "post_max_size")
                                if self.upload_max_filesize != self.upload_max_filesize_end:
                                    self.message_set_phpini(self.sub_domain_end, self.upload_max_filesize[0], "upload_max_filesize")

                                self._log.debug("Source subdomain - {} - {}".format(self.sub_domain, self.php_version))
                                self._log.debug("Destination subdomain - {} - {}".format(self.sub_domain_end, self.php_version_end))
                            else:
                                self._log.error("phpinfo subdomain not found - {} - {} - {}".format(self.values_ticket, self.sub_domain, self.sub_domain_end))

                except Exception as er:
                    self._log.error("Failed handled phpinfo subdomains - {} - {}".format(self.values_ticket, er))
                    continue

        except Exception as er:
            # generate a error log
            self._log.error("phpinfo subdomains - {} - {}".format(self.__class__.__name__, er))
            return False

    def handle_phpinfo_addondomains(self):
        try:
            for self.addon_domain in self.addon_domains:
                self.php_version = None
                self.allow_url_fopen = None
                self.max_input_vars = None
                self.max_execution_time = None
                self.memory_limit = None
                self.post_max_size = None
                self.upload_max_filesize = None
                self.php_version_end = None
                self.allow_url_fopen_end = None
                self.max_input_vars_end = None
                self.max_execution_time_end = None
                self.memory_limit_end = None
                self.post_max_size_end = None
                self.upload_max_filesize_end = None
                self.file_phpinfo = None
                self.file_phpinfo_end = None
                self.open_phpinfo = None
                self.open_phpinfo_end = None
                self.result_phpinfo = None
                self.result_phpinfo_end = None
                try:
                    for self.addon_domain_end in self.addon_domains_end:
                        if self.addon_domain == self.addon_domain_end:
                            self.file_phpinfo = os.path.join(self.report_casepath, "source/" + self.addon_domain + ".json")
                            self.file_phpinfo_end = os.path.join(self.report_casepath, "destination_end/" + self.addon_domain_end + ".json")
                            if os.path.exists(self.file_phpinfo) and os.path.exists(self.file_phpinfo_end):
                                with closing(open(self.file_phpinfo)) as self.open_phpinfo:
                                    self.result_phpinfo = ast.literal_eval(json.load(self.open_phpinfo))
                                    self.php_version = "".join(self.result_phpinfo['Core']['PHP Version'].split(".")[:2])
                                    self.allow_url_fopen = self.result_phpinfo['Core']['allow_url_fopen']
                                    self.max_input_vars = self.result_phpinfo['Core']['max_input_vars']
                                    self.max_execution_time = self.result_phpinfo['Core']['max_execution_time']
                                    self.memory_limit = self.result_phpinfo['Core']['memory_limit']
                                    self.post_max_size = self.result_phpinfo['Core']['post_max_size']
                                    self.upload_max_filesize = self.result_phpinfo['Core']['upload_max_filesize']

                                with closing(open(self.file_phpinfo_end)) as self.open_phpinfo_end:
                                    self.result_phpinfo_end = ast.literal_eval(json.load(self.open_phpinfo_end))
                                    self.php_version_end = "".join(self.result_phpinfo_end['Core']['PHP Version'].split(".")[:2])
                                    self.allow_url_fopen_end = self.result_phpinfo_end['Core']['allow_url_fopen']
                                    self.max_input_vars_end = self.result_phpinfo_end['Core']['max_input_vars']
                                    self.max_execution_time_end = self.result_phpinfo_end['Core']['max_execution_time']
                                    self.memory_limit_end = self.result_phpinfo_end['Core']['memory_limit']
                                    self.post_max_size_end = self.result_phpinfo_end['Core']['post_max_size']
                                    self.upload_max_filesize_end = self.result_phpinfo_end['Core']['upload_max_filesize']

                                if self.php_version != self.php_version_end:
                                    if self.request_type == 1:
                                        if int(self.php_version) < 70:
                                            self.message_set_phpversion(self.addon_domain_end, "70")
                                        else:
                                            self.message_set_phpversion(self.addon_domain_end, self.php_version)
                                    else:
                                        self.message_set_phpversion(self.addon_domain_end, self.php_version)
                                if self.allow_url_fopen != self.allow_url_fopen_end:
                                    self.message_set_phpini(self.addon_domain_end, self.allow_url_fopen[0], "allow_url_fopen")
                                if self.max_input_vars != self.max_input_vars_end:
                                    self.message_set_phpini(self.addon_domain_end, self.max_input_vars[0], "max_input_vars")
                                if self.max_execution_time != self.max_execution_time_end:
                                    self.message_set_phpini(self.addon_domain_end, self.max_execution_time[0], "max_execution_time")
                                if self.memory_limit != self.memory_limit_end:
                                    self.message_set_phpini(self.addon_domain_end, self.memory_limit[0], "memory_limit")
                                if self.post_max_size != self.post_max_size_end:
                                    self.message_set_phpini(self.addon_domain_end, self.post_max_size[0], "post_max_size")
                                if self.upload_max_filesize != self.upload_max_filesize_end:
                                    self.message_set_phpini(self.addon_domain_end, self.upload_max_filesize[0], "upload_max_filesize")

                                self._log.debug("Source addon domain - {} - {}".format(self.addon_domain, self.php_version))
                                self._log.debug("Destination addon domain - {} - {}".format(self.addon_domain_end, self.php_version_end))
                            else:
                                self._log.error("phpinfo addon domain not found - {} - {} - {}".format(self.values_ticket, self.addon_domain, self.addon_domain_end))

                except Exception as er:
                    self._log.error("Failed handled phpinfo addon domain - {} - {}".format(self.values_ticket, er))
                    continue

        except Exception as er:
            # generate a error log
            self._log.error("phpinfo addon domains - {} - {}".format(self.__class__.__name__, er))
            return False

    def handle_phpinfo_parkeddomains(self):
        try:
            for self.parked_domain in self.parked_domains:
                self.php_version = None
                self.allow_url_fopen = None
                self.max_input_vars = None
                self.max_execution_time = None
                self.memory_limit = None
                self.post_max_size = None
                self.upload_max_filesize = None
                self.php_version_end = None
                self.allow_url_fopen_end = None
                self.max_input_vars_end = None
                self.max_execution_time_end = None
                self.memory_limit_end = None
                self.post_max_size_end = None
                self.upload_max_filesize_end = None
                self.file_phpinfo = None
                self.file_phpinfo_end = None
                self.open_phpinfo = None
                self.open_phpinfo_end = None
                self.result_phpinfo = None
                self.result_phpinfo_end = None
                try:
                    for self.parked_domain_end in self.parked_domains_end:
                        if self.parked_domain == self.parked_domain_end:
                            self.file_phpinfo = os.path.join(self.report_casepath, "source/" + self.parked_domain + ".json")
                            self.file_phpinfo_end = os.path.join(self.report_casepath, "destination_end/" + self.parked_domain_end + ".json")
                            if os.path.exists(self.file_phpinfo) and os.path.exists(self.file_phpinfo_end):
                                with closing(open(self.file_phpinfo)) as self.open_phpinfo:
                                    self.result_phpinfo = ast.literal_eval(json.load(self.open_phpinfo))
                                    self.php_version = "".join(self.result_phpinfo['Core']['PHP Version'].split(".")[:2])
                                    self.allow_url_fopen = self.result_phpinfo['Core']['allow_url_fopen']
                                    self.max_input_vars = self.result_phpinfo['Core']['max_input_vars']
                                    self.max_execution_time = self.result_phpinfo['Core']['max_execution_time']
                                    self.memory_limit = self.result_phpinfo['Core']['memory_limit']
                                    self.post_max_size = self.result_phpinfo['Core']['post_max_size']
                                    self.upload_max_filesize = self.result_phpinfo['Core']['upload_max_filesize']

                                with closing(open(self.file_phpinfo_end)) as self.open_phpinfo_end:
                                    self.result_phpinfo_end = ast.literal_eval(json.load(self.open_phpinfo_end))
                                    self.php_version_end = "".join(self.result_phpinfo_end['Core']['PHP Version'].split(".")[:2])
                                    self.allow_url_fopen_end = self.result_phpinfo_end['Core']['allow_url_fopen']
                                    self.max_input_vars_end = self.result_phpinfo_end['Core']['max_input_vars']
                                    self.max_execution_time_end = self.result_phpinfo_end['Core']['max_execution_time']
                                    self.memory_limit_end = self.result_phpinfo_end['Core']['memory_limit']
                                    self.post_max_size_end = self.result_phpinfo_end['Core']['post_max_size']
                                    self.upload_max_filesize_end = self.result_phpinfo_end['Core']['upload_max_filesize']

                                if self.php_version != self.php_version_end:
                                    if self.request_type == 1:
                                        if int(self.php_version) < 70:
                                            self.message_set_phpversion(self.parked_domain_end, "70")
                                        else:
                                            self.message_set_phpversion(self.parked_domain_end, self.php_version)
                                    else:
                                        self.message_set_phpversion(self.parked_domain_end, self.php_version)
                                if self.allow_url_fopen != self.allow_url_fopen_end:
                                    self.message_set_phpini(self.parked_domain_end, self.allow_url_fopen[0], "allow_url_fopen")
                                if self.max_input_vars != self.max_input_vars_end:
                                    self.message_set_phpini(self.parked_domain_end, self.max_input_vars[0], "max_input_vars")
                                if self.max_execution_time != self.max_execution_time_end:
                                    self.message_set_phpini(self.parked_domain_end, self.max_execution_time[0], "max_execution_time")
                                if self.memory_limit != self.memory_limit_end:
                                    self.message_set_phpini(self.parked_domain_end, self.memory_limit[0], "memory_limit")
                                if self.post_max_size != self.post_max_size_end:
                                    self.message_set_phpini(self.parked_domain_end, self.post_max_size[0], "post_max_size")
                                if self.upload_max_filesize != self.upload_max_filesize_end:
                                    self.message_set_phpini(self.parked_domain_end, self.upload_max_filesize[0], "upload_max_filesize")

                                self._log.debug("Source parked domains - {} - {}".format(self.parked_domain, self.php_version))
                                self._log.debug("Destination parked domains - {} - {}".format(self.parked_domain_end, self.php_version_end))
                            else:
                                self._log.error("phpinfo parked domain not found - {} - {} - {}".format(self.values_ticket, self.parked_domain, self.parked_domain_end))

                except Exception as er:
                    self._log.error("Failed handled phpinfo parked domains - {} - {}".format(self.values_ticket, er))
                    continue

        except Exception as er:
            # generate a error log
            self._log.error("phpinfo parked domains - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_set_phpversion(self, set_domain, set_version_php):
        try:
            self.set_domain = set_domain
            self.set_version_php = set_version_php
            self.message = dict()
            self.message.update({'type_task': 'phpversion'})
            self.message.update({'set_version_php': self.set_version_php})
            self.message.update({'set_domain': self.set_domain})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_handle_php.publish(self.message)
            self._log.debug("message_set_phpversion - {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message check - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_set_phpini(self, set_domain, set_value_php, set_variable_php):
        try:
            self.set_domain = set_domain
            self.set_value_php = set_value_php
            self.set_variable_php = set_variable_php
            self.message = dict()
            self.message.update({'type_task': 'phpini'})
            self.message.update({'set_variable_php': self.set_variable_php})
            self.message.update({'set_value_php': self.set_value_php})
            self.message.update({'set_domain': self.set_domain})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_handle_php.publish(self.message)
            self._log.debug("message_set_phpini - {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message check - {} - {}".format(self.__class__.__name__, er))
            return False
