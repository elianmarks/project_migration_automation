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

# custom libraries
from migration_automation_manager.module_log import ModuleLog
from migration_automation_manager.module_zen import ModuleZen
from migration_automation_manager.module_templates import ModuleTemplates
from migration_automation_manager.module_regex import ModuleRegex
from migration_automation_manager.module_dns import ModuleDNS
from migration_automation_manager.module_configuration import ModuleConfiguration
from migration_automation_manager.module_publish import ModulePublish
from migration_automation_manager.module_database import ModuleDatabase
from migration_automation_manager.module_ansible import ModuleAnsible
import uuid
import os
import json
import time
from contextlib import closing


class ModuleDBCheck:

    def __init__(self, development=None):
        try:
            self.development = development
            self.module_configuration = None
            self.module_log = None
            # load the conf
            if not self.config_init():
                exit(3)
            # instance of the modules
            self.module_regex = ModuleRegex(self.module_log.log, self.module_configuration)
            self.module_dns = ModuleDNS(self.module_log.log, self.module_configuration)
            self.module_zen = ModuleZen(self.module_log.log, self.module_configuration)
            self.module_templates = ModuleTemplates(self.module_log.log)
            self.module_database = ModuleDatabase(self.module_log.log, self.module_configuration)
            self.playbook_check = self.module_configuration.playbook_check
            # variables
            self._log = self.module_log.log
            self.summary_ansible = None
            self.module_ansible = None
            self.vars_ansible = None
            self.request_type = None
            self.ns_server = None
            self.zen_return = None
            self.message = None
            self.info_list = list()
            self.ticket_id = None
            self.main_domain = None
            self.result_register = None
            self.line_register = None
            self.general_error = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.type_problem = None
            self.check_message = None
            self.thread_id = None
            self.main_account = None
            self.force_ns = None
            self.result_owners = None
            self.line_owner = None
            self.general_error_allusers = None
            self.this_owner = None
            self.specific_migration = None
            self.list_values = None
            self.src_server_owner = None
            self.dst_server_owner = None
            self.main_domain_owner = None
            self.ticket_id_owner = None
            self.force_ns_owner = None
            self.thread_id_owner = None
            self.user_owner = None
            self.general_error_owner = None
            self.report_casepath = None
            self.specific_migration_owner = None
            self.list_migration_owner = None
            self.file_reseller_accounts_data = None
            self.open_reseller_accounts_data = None
            self.result_reseller_accounts_data = None
            self.specific_migration_allusers = None
            self.list_migration_allusers = None
            self.file_allusers_accounts_data = None
            self.open_allusers_accounts_data = None
            self.result_allusers_accounts_data = None
            self.result_clients = None
            self.result_allusers = None
            self.line_allusers = None
            self.all_users = None
            self.server = None
            self.src_server_allusers = None
            self.dst_server_allusers = None
            self.main_domain_allusers = None
            self.ticket_id_allusers = None
            self.force_ns_allusers = None
            self.specific_migration_allusers = None
            self.thread_id_allusers = None
            self.list_migration_allusers = None
            self.check_clients = None
            self.count_clients_db = None
            self.file_ns_zones = None
            self.open_ns_zones = None
            self.ns_zones = None
            self.result_check = None
            self.thread_id_results = None
            self.ticket_id_results = None
            self.user_results = None
            self.list_migration = None
            self.main_domain_results = None
            self.specific_migration_results = None
            self.count_specific_migration = None
            self.file_reseller_accounts = None
            self.result_reseller_accounts = None
            self.open_reseller_accounts = None
            self.count_clients_json = None
            self.results_completed = None
            self.users_error_check = None
            self.users_error_check_list = None
            self.thread_id_check = None
            self.ticket_id_check = None
            self.user_check = None
            self.main_domain_check = None
            self.status_check = None
            self.results_completed = None
            self.all_users_results = None
            self.check_allusers_results = None
            self.this_owner_results = None
            self.check_clients_results = None
            self.file_domain_user_data = None
            self.open_domain_user_data = None
            self.result_domain_user_data = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
            self.src_ip_allusers = None
            self.dst_ip_allusers = None
            self.connect_ip_allusers = None
            self.dst_ip_owner = None
            self.src_ip_owner = None
            self.connect_ip_owner = None
            self.thread_id_shared = None
            self.ticket_id_shared = None
            self.user_shared = None
            self.main_domain_shared = None
            self.user = None
            self.home = None
            self.brand = None
            self.brand_owner = None
            self.brand_allusers = None
            self.file_flag_account_suspended = None
            self.report_dir = self.module_configuration.report_dir
            self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
            self.queue_manager = ModulePublish(self._log, "manager", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                               self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("manager"))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            # exit the application with code 4
            exit(4)

    def clean_variables(self):
        try:
            # clean variables
            self.ticket_id = None
            self.main_domain = None
            self.general_error = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.type_problem = None
            self.check_message = None
            self.thread_id = None
            self.request_type = None
            self.ns_server = None
            self.zen_return = None
            self.message = None
            self.force_ns = None
            self.this_owner = None
            self.all_users = None
            self.server = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
            self.specific_migration = None

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            self.general_error = True
            return False

    def config_init(self):
        try:
            # instance module configuration
            self.module_configuration = ModuleConfiguration(self.development)
            if self.module_configuration is not None and not self.module_configuration.initialize():
                # only print the error, since module_log there isn't instance
                print("Error in ModuleConfiguration")
                return False
            else:
                # instance the module_log class
                self.module_log = ModuleLog(self.module_configuration, 14)
                if self.module_log is not None and not self.module_log.initialize():
                    print("Error in initialize ModuleLog")
                    return False
                else:
                    return True

        except Exception as er:
            # only print the error, since ModuleLog there isn't instance
            print("{} - {}".format(__name__, er))
            return False

    def message_manager(self, main_account=None):
        try:
            self.main_account = main_account
            self.message = dict()
            if self.main_account:
                self.message.update({'sender': 'check'})
                self.message.update({'type_task': "destination"})
            else:
                self.message.update({'sender': 'bdcheck'})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_manager.publish(self.message)
            self._log.info("Send manager {}".format(self.message))
            self.check_message = True

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            self.general_error = True
            return False

    def check_type(self):
        try:
            self.src_type = self.module_regex.check_type(self.src_server)
            self.dst_type = self.module_regex.check_type(self.dst_server)
            if self.src_type is not False and self.dst_type is not False:
                return True
            else:
                self._log.error("check_type failed in src_type or dst_type")
                self.general_error = True
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            self.general_error = True
            return False

    def check_ns(self):
        try:
            self.ns_server = self.module_dns.dns_resolver(self.main_domain, "NS")
            if self.ns_server is not False and self.module_regex.check_ns(self.ns_server):
                return True
            else:
                self._log.debug("check_ns failed in ns_server - {}".format(self.ns_server))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            self.general_error = True
            return False

    def apply_error(self, brand="br"):
        try:
            self.brand = brand
            # comment in ticket
            self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Apply error", self.thread_id), public=False, brand=self.brand)
            # get ticket object
            self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
            if self.zen_return is not False:
                # update status analyzing
                self.module_database.update_analyzing("status", 2, thread_id=self.thread_id)
                # update analyzing
                self.module_database.update_analyzing("handled", 0, thread_id=self.thread_id)
                # update ticket
                self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search)
                self.zen_return.assignee = None
                self.zen_return.status = "open"
                # apply the change in ticket
                self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                # generate a info log
                self._log.info("apply_error in - '{}'".format(self.ticket_id))

        except Exception as er:
            # generate a error log
            self._log.error("apply_error - {} - {} - {}".format(__name__, er, self.ticket_id))
            return False

    def apply_send_queue(self, type_problem, brand="br"):
        try:
            self.brand = brand
            self.type_problem = type_problem
            if self.type_problem == "NS":
                # comment in ticket
                self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Not using NS to shared server."
                                                                                             "\n\nNS1: {}".format(self.ns_server), self.thread_id), public=False, brand=self.brand)
            # get ticket object
            self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
            if self.zen_return is not False:
                # update ticket
                self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_ns_not, self.module_zen.tag_search)
                self.zen_return.assignee = None
                self.zen_return.status = "open"
                # apply the change in ticket
                self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                # generate a info log
                self._log.info("apply_send_queue in - '{}'".format(self.ticket_id))
                # update handled
                self.module_database.update_analyzing("handled", 0, thread_id=self.thread_id)
                # update status
                self.module_database.update_analyzing("status", 2, thread_id=self.thread_id)

        except Exception as er:
            # generate a error log
            self._log.error("apply_send_queue - {} - {} - {}".format(__name__, er, self.ticket_id))
            return False

    def apply_database(self):
        try:
            # update analyzing
            self.module_database.update_analyzing("status", 1, thread_id=self.thread_id)
            self.module_database.update_analyzing("request_type", self.request_type, thread_id=self.thread_id)
            self.module_database.update_analyzing("handled", 1, thread_id=self.thread_id)
            self.module_database.update_analyzing("src_type", self.src_type, thread_id=self.thread_id)
            self.module_database.update_analyzing("dst_type", self.dst_type, thread_id=self.thread_id)
            self.module_database.update_analyzing("thread_id_main", self.thread_id, thread_id=self.thread_id)

        except Exception as er:
            # generate a error log
            self._log.error("apply_database - {} - {} - {}".format(__name__, er, self.ticket_id))
            self.general_error = True
            return False

    def apply_database_client(self):
        try:
            if self.module_database.insert_analyzing(self.ticket_id, thread_id=self.thread_id):
                self.module_database.update_analyzing("status", 1, thread_id=self.thread_id)
                self.module_database.update_analyzing("request_type", self.request_type, thread_id=self.thread_id)
                self.module_database.update_analyzing("handled", 1, thread_id=self.thread_id)
                self.module_database.update_analyzing("register_type", 3, thread_id=self.thread_id)
                self.module_database.update_analyzing("src_server", self.src_server, thread_id=self.thread_id)
                self.module_database.update_analyzing("dst_server", self.dst_server, thread_id=self.thread_id)
                self.module_database.update_analyzing("src_type", self.src_type, thread_id=self.thread_id)
                self.module_database.update_analyzing("dst_type", self.dst_type, thread_id=self.thread_id)
                self.module_database.update_analyzing("main_domain", self.main_domain, thread_id=self.thread_id)
                self.module_database.update_analyzing("owner", self.user_owner, thread_id=self.thread_id)
                self.module_database.update_analyzing("force_ns", self.force_ns_owner, thread_id=self.thread_id)
                self.module_database.update_analyzing("client", 1, thread_id=self.thread_id)
                self.module_database.update_analyzing("thread_id_main", self.thread_id_owner, thread_id=self.thread_id)
                self.module_database.update_analyzing("brand", self.brand_owner, thread_id=self.thread_id)
                if self.connect_ip_owner is not None and self.connect_ip_owner is not False and self.connect_ip_owner == 1:
                    self.module_database.update_analyzing("connect_ip", self.connect_ip_owner, thread_id=self.thread_id)
                    if self.src_ip_owner is not None and self.src_ip_owner is not False:
                        self.module_database.update_analyzing("src_ip", self.src_ip_owner, thread_id=self.thread_id)
                    if self.dst_ip_owner is not None and self.dst_ip_owner is not False:
                        self.module_database.update_analyzing("dst_ip", self.dst_ip_owner, thread_id=self.thread_id)
            else:
                self._log.error("insert in apply_database_client - '{}' - '{}'".format(self.ticket_id, self.main_domain))
                self.general_error = True

        except Exception as er:
            # generate a error log
            self._log.error("apply_database_client - {} - {} - {} - {}".format(__name__, er, self.ticket_id, self.main_domain))
            self.general_error = True
            return False

    def apply_database_allusers(self):
        try:
            if self.module_database.insert_analyzing(self.ticket_id, thread_id=self.thread_id):
                self.module_database.update_analyzing("status", 1, thread_id=self.thread_id)
                self.module_database.update_analyzing("request_type", self.request_type, thread_id=self.thread_id)
                self.module_database.update_analyzing("handled", 1, thread_id=self.thread_id)
                self.module_database.update_analyzing("register_type", 4, thread_id=self.thread_id)
                self.module_database.update_analyzing("src_server", self.src_server, thread_id=self.thread_id)
                self.module_database.update_analyzing("dst_server", self.dst_server, thread_id=self.thread_id)
                self.module_database.update_analyzing("src_type", self.src_type, thread_id=self.thread_id)
                self.module_database.update_analyzing("dst_type", self.dst_type, thread_id=self.thread_id)
                self.module_database.update_analyzing("main_domain", self.main_domain, thread_id=self.thread_id)
                self.module_database.update_analyzing("client", 1, thread_id=self.thread_id)
                self.module_database.update_analyzing("thread_id_main", self.thread_id_allusers, thread_id=self.thread_id)
                self.module_database.update_analyzing("brand", self.brand_allusers, thread_id=self.thread_id)
                if self.connect_ip_allusers is not None and self.connect_ip_allusers is not False and self.connect_ip_allusers == 1:
                    self.module_database.update_analyzing("connect_ip", self.connect_ip_allusers, thread_id=self.thread_id)
                    if self.src_ip_allusers is not None and self.src_ip_allusers is not False:
                        self.module_database.update_analyzing("src_ip", self.src_ip_allusers, thread_id=self.thread_id)
                    if self.dst_ip_allusers is not None and self.dst_ip_allusers is not False:
                        self.module_database.update_analyzing("dst_ip", self.dst_ip_allusers, thread_id=self.thread_id)
            else:
                self._log.error("insert in apply_database_allusers - '{}' - '{}'".format(self.ticket_id, self.main_domain))
                self.general_error = True

        except Exception as er:
            # generate a error log
            self._log.error("apply_database_allusers - {} - {} - {} - {}".format(__name__, er, self.ticket_id, self.main_domain))
            self.general_error = True
            return False

    def handle_info(self, brand="br"):
        try:
            self.brand = brand
            self.info_list = list()
            self.info_list.append(self.thread_id)
            self.info_list.append(self.src_type)
            self.info_list.append(self.src_server)
            self.info_list.append(self.dst_type)
            self.info_list.append(self.dst_server)
            self.info_list.append(self.main_domain)
            self.info_list.append(self.request_type)
            self.module_zen.comment_ticket(self.ticket_id, self.module_templates.info_started(self.info_list), public=False, brand=self.brand)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("handle_info - {} - {} - {}".format(__name__, er, self.ticket_id))
            return False

    def set_values(self, list_values):
        try:
            self.list_values = list_values
            self.src_server = self.list_values[0]
            self.dst_server = self.list_values[1]
            self.main_domain = self.list_values[2]
            self.ticket_id = int(self.list_values[3])
            self.force_ns = int(self.list_values[4])
            self.specific_migration = int(self.list_values[5])
            self.this_owner = int(self.list_values[6])
            self.all_users = int(self.list_values[7])
            if self.list_values[8] is not None and "," in self.list_values[8]:
                self.list_migration = self.list_values[8].split(",")
            else:
                self.list_migration = list()
                self.list_migration.append(self.list_values[8])
            self.src_ip = self.list_values[9]
            self.dst_ip = self.list_values[10]
            self.connect_ip = self.list_values[11]
            self.brand = self.list_values[12]
            return True

        except Exception as er:
            # generate a error log
            self._log.error("set_values - {} - {} - {}".format(__name__, er, self.ticket_id))
            return False

    def apply_duplicated(self, brand="br"):
        try:
            self.brand = brand
            # comment in ticket
            # self.zen_return = self.module_zen.macro(self.ticket_id, self.module_zen.macro_start_id)
            if self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Migration duplicated", self.main_domain), public=False, brand=self.brand):
                if not self.general_error:
                    self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                    if self.zen_return is not False:
                        # update ticket
                        self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search)
                        self.zen_return.status = "open"
                        # apply the change in ticket
                        self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                        # generate a info log
                        self._log.info("apply_duplicated in - '{}'".format(self.ticket_id))
            else:
                self._log.error("Comment duplicated ticket failed in apply_duplicated - {} - {}".format(self.ticket_id, self.main_domain))

        except Exception as er:
            # generate a error log
            self._log.error("apply_duplicated - {} - {} - {}".format(__name__, er, self.ticket_id))
            self.general_error = True
            return False

    def apply_migration(self, brand="br"):
        try:
            self.brand = brand
            # comment in ticket
            # self.zen_return = self.module_zen.macro(self.ticket_id, self.module_zen.macro_start_id)
            if self.module_zen.comment_ticket(self.ticket_id, self.module_templates.all_started(brand=self.brand), brand=self.brand):
                self.apply_database()
                if not self.general_error:
                    self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                    if self.zen_return is not False:
                        # update ticket
                        self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_handled, self.module_zen.tag_search)
                        self.zen_return.status = "pending"
                        # apply the change in ticket
                        self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                        # generate a info log
                        self._log.info("apply_migration in - '{}'".format(self.ticket_id))
            else:
                self._log.error("Comment started ticket failed in apply_migration - {} - {}".format(self.ticket_id, self.thread_id))

        except Exception as er:
            # generate a error log
            self._log.error("apply_migration - {} - {} - {}".format(__name__, er, self.ticket_id))
            self.general_error = True
            return False

    def get_ns_zones(self):
        try:
            self.ns_zones = False
            self.file_ns_zones = os.path.join(self.report_casepath, "destination_end/nsZones")
            # check if file exists
            if os.path.exists(self.file_ns_zones):
                # open file and store in variable
                with closing(open(self.file_ns_zones)) as self.open_ns_zones:
                    self.ns_zones = self.open_ns_zones.read().splitlines()
                    return True
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("Get ns zones in bdcheck {} - {}".format(self.__class__.__name__, er))
            return False

    def check_results(self):
        try:
            self.apply_results(self.module_database.get_results_reseller())
            self.apply_results(self.module_database.get_results_allusers())
            self.apply_results_shared(self.module_database.get_results_shared())
            self._log.info("Entering in sleep - 10 minutes")

        except Exception as er:
            # generate a error log
            self._log.error("check_results {} - {}".format(self.__class__.__name__, er))
            return False

    def apply_results_shared(self, result_check):
        try:
            self.result_check = result_check
            if self.result_check is not None and self.result_check is not False and len(self.result_check) > 0:
                for self.line_check in self.result_check:
                    try:
                        self.thread_id_shared = self.line_check[0]
                        self.ticket_id_shared = self.line_check[1]
                        self.user_shared = self.line_check[2]
                        self.main_domain_shared = self.line_check[3]
                        self.brand = self.line_check[4]
                        self.report_casepath = os.path.join(self.report_dir, str(self.main_domain_shared) + "_" + str(self.ticket_id_shared) + "_" + str(self.thread_id_shared))
                        if self.get_ns_zones() and self.ns_zones is not False and self.ns_zones is not None and len(self.ns_zones) == 2:
                            if self.module_zen.comment_ticket(self.ticket_id_shared, self.module_templates.shared_completed(self.ns_zones, brand=self.brand), brand=self.brand):
                                self.zen_return = self.module_zen.search_id(self.ticket_id_shared, brand=self.brand)
                                time.sleep(3)
                                if self.zen_return is not False:
                                    self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_completed, self.module_zen.tag_search)
                                    self.zen_return.assignee = None
                                    self.zen_return.status = "pending"
                                    self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                    self.module_database.update_analyzing("end_ticket", 3, self.thread_id_shared)
                                    self._log.info("Completed ticket - {} - {}".format(self.ticket_id_shared, self.user_shared))
                            else:
                                self._log.error("Comment completed ticket failed - {} - {}".format(self.ticket_id_check, self.user_shared))
                        else:
                            self._log.info("Failed get values in file_ns_zones")
                            if self.module_zen.comment_ticket(self.ticket_id_check, self.module_zen.comment_error("Error in get and handle ns zones", self.thread_id_shared), public=False, brand=self.brand):
                                self.zen_return = self.module_zen.search_id(self.ticket_id_shared, brand=self.brand)
                                time.sleep(3)
                                if self.zen_return is not False:
                                    self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search)
                                    self.zen_return.assignee = None
                                    self.zen_return.status = "open"
                                    self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                    self.module_database.update_analyzing("end_ticket", 2, self.thread_id_shared)
                                    self._log.info("Completed ticket - {} - {}".format(self.ticket_id_shared, self.user_shared))
                            else:
                                self._log.error("Comment completed ticket failed - {} - {}".format(self.ticket_id_shared, self.user_shared))

                    except Exception as er:
                        # generate a error log
                        self._log.error("for result_check - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id))
                        continue

        except Exception as er:
            # generate a error log
            self._log.error("apply_results - {} - {}".format(__name__, er))
            self.general_error = True
            return False

    def apply_results(self, result_check):
        try:
            self.result_check = result_check
            if self.result_check is not None and self.result_check is not False and len(self.result_check) > 0:
                for self.line_check in self.result_check:
                    try:
                        self.thread_id_results = self.line_check[0]
                        self.ticket_id_results = self.line_check[1]
                        self.user_results = self.line_check[2]
                        self.main_domain_results = self.line_check[3]
                        self.specific_migration_results = self.line_check[4]
                        self.count_specific_migration = self.line_check[5]
                        self.all_users_results = self.line_check[6]
                        self.check_allusers_results = self.line_check[7]
                        self.this_owner_results = self.line_check[8]
                        self.check_clients_results = self.line_check[9]
                        self.brand = self.line_check[10]
                        self.check_clients = self.module_database.get_check_clients(self.thread_id_results)
                        if self.check_clients is not None and self.check_clients is not False and len(self.check_clients) > 0:
                            for self.line_clients in self.check_clients:
                                self.thread_id_check = self.line_clients[0]
                                self.ticket_id_check = self.line_clients[1]
                                self.user_check = self.line_clients[2]
                                self.main_domain_check = self.line_clients[3]
                                self.status_check = self.line_clients[4]
                                if self.status_check == 3:
                                    self.info_list = list()
                                    self.info_list.append(self.thread_id_check)
                                    self.info_list.append(self.thread_id_results)
                                    self.info_list.append(self.main_domain_check)
                                    self.info_list.append(self.user_check)
                                    self.module_zen.comment_ticket(self.ticket_id_check, self.module_templates.info_completed(self.info_list), public=False, brand=self.brand)
                                    self.module_database.update_analyzing("client", 3, self.thread_id_check)
                                    self.module_database.update_analyzing("end_tasks", 1, self.thread_id_check)
                                elif self.status_check == 2:
                                    self.info_list = list()
                                    self.info_list.append(self.thread_id_check)
                                    self.info_list.append(self.thread_id_results)
                                    self.info_list.append(self.main_domain_check)
                                    self.info_list.append(self.user_check)
                                    self.module_zen.comment_ticket(self.ticket_id_check, self.module_templates.info_failed(self.info_list), public=False, brand=self.brand)
                                    self.module_database.update_analyzing("client", 2, self.thread_id_check)
                                    self.module_database.update_analyzing("end_tasks", 1, self.thread_id_check)
                        self.check_clients = None
                        self.count_clients_json = None
                        self.check_clients, self.count_clients_db = self.module_database.get_check_completed(self.thread_id_results)
                        self.report_casepath = os.path.join(self.report_dir, str(self.main_domain_results) + "_" + str(self.ticket_id_results) + "_" + str(self.thread_id_results))
                        if self.check_clients is not None and self.check_clients is not False and self.count_clients_db is not None and self.count_clients_db is not False and len(self.check_clients) > 0:
                            if self.specific_migration_results == 0:
                                if self.this_owner_results == 1 and self.check_clients_results == 3:
                                    self.file_reseller_accounts = os.path.join(self.report_casepath, "source/reseller_accounts.json")
                                    if os.path.exists(self.file_reseller_accounts):
                                        self.count_clients_json = None
                                        with closing(open(self.file_reseller_accounts)) as self.open_reseller_accounts:
                                            self.result_reseller_accounts = json.load(self.open_reseller_accounts)
                                            if self.result_reseller_accounts['metadata']['result'] == 1 and self.result_reseller_accounts['metadata']['reason'] == "OK":
                                                self.count_clients_json = self.result_reseller_accounts['data']['reseller']['active']
                                            else:
                                                self._log.info("Failed get values in - {}".format(self.file_reseller_accounts))
                                    else:
                                        self._log.info("File not found - {}".format(self.file_reseller_accounts))
                                elif self.all_users_results == 3 and self.check_allusers_results == 3:
                                    self.file_allusers_accounts_data = os.path.join(self.report_casepath, "source/list_accts.json")
                                    if os.path.exists(self.file_allusers_accounts_data):
                                        self.count_clients_json = None
                                        with closing(open(self.file_allusers_accounts_data)) as self.open_allusers_accounts_data:
                                            self.result_allusers_accounts_data = json.load(self.open_allusers_accounts_data)
                                            if self.result_allusers_accounts_data['metadata']['result'] == 1 and self.result_allusers_accounts_data['metadata']['reason'] == "OK":
                                                self.count_clients_json = len(self.result_allusers_accounts_data['data']['acct'])
                                            else:
                                                self._log.info("Failed get values in - {}".format(self.file_allusers_accounts_data))
                                    else:
                                        self._log.info("File not found - {}".format(self.file_allusers_accounts_data))
                                else:
                                    self._log.info("Not match in check reseller or vps / dedi - {} - {}".format(self.thread_id_results, self.ticket_id_results))
                            elif self.specific_migration_results == 1:
                                self.count_clients_json = self.count_specific_migration
                            if self.count_clients_db is not None and self.count_clients_db is not False and \
                                    self.count_clients_json is not None and self.count_clients_json is not False and \
                                    int(self.count_clients_db) == int(self.count_clients_json):
                                self.results_completed = True
                                self.users_error_check = dict()
                                self.users_error_check_list = list()
                                for self.line_clients in self.check_clients:
                                    self.thread_id_check = self.line_clients[0]
                                    self.ticket_id_check = self.line_clients[1]
                                    self.user_check = self.line_clients[2]
                                    self.main_domain_check = self.line_clients[3]
                                    self.status_check = self.line_clients[4]
                                    if self.status_check != 3:
                                        self.results_completed = False
                                        self.users_error_check.update({'user': self.user_check})
                                        self.users_error_check.update({'thread_id': self.thread_id_check})
                                        self.users_error_check.update({'main_domain': self.main_domain_check})
                                        self.users_error_check_list.append(str(self.users_error_check))
                                if self.results_completed and len(self.users_error_check_list) == 0:
                                    if self.get_ns_zones() and self.ns_zones is not False and self.ns_zones is not None and len(self.ns_zones) == 2:
                                        if (self.this_owner_results == 1 and self.check_clients_results == 3 and self.module_zen.comment_ticket(self.ticket_id_results, self.module_templates.reseller_completed(self.ns_zones, brand=self.brand), brand=self.brand)) or \
                                                (self.all_users_results == 3 and self.check_allusers_results == 3 and self.module_zen.comment_ticket(self.ticket_id_results, self.module_templates.allusers_completed(self.ns_zones, brand=self.brand), brand=self.brand)):
                                            self.zen_return = self.module_zen.search_id(self.ticket_id_results, brand=self.brand)
                                            time.sleep(3)
                                            if self.zen_return is not False:
                                                self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_completed, self.module_zen.tag_search)
                                                self.zen_return.assignee = None
                                                self.zen_return.status = "pending"
                                                self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                                self.module_database.update_analyzing("end_ticket", 3, self.thread_id_results)
                                                self._log.info("Completed ticket - {} - {}".format(self.ticket_id_results, self.user_results))
                                        else:
                                            self._log.error("Comment completed ticket failed - {} - {}".format(self.ticket_id_check, self.user_results))
                                    else:
                                        self._log.info("Failed get values in file_ns_zones")
                                        if self.module_zen.comment_ticket(self.ticket_id_check, self.module_zen.comment_error("Error in get and handle ns zones", self.thread_id_results), public=False, brand=self.brand):
                                            self.zen_return = self.module_zen.search_id(self.ticket_id_results, brand=self.brand)
                                            time.sleep(3)
                                            if self.zen_return is not False:
                                                self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search)
                                                self.zen_return.assignee = None
                                                self.zen_return.status = "open"
                                                self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                                self.module_database.update_analyzing("end_ticket", 2, self.thread_id_results)
                                                self._log.info("Completed ticket - {} - {}".format(self.ticket_id_results, self.user_results))
                                        else:
                                            self._log.error("Comment completed ticket failed - {} - {}".format(self.ticket_id_results, self.user_results))
                                else:
                                    if self.module_zen.comment_ticket(self.ticket_id_check, self.module_zen.comment_error("Error migration users\n\n'{}'.".format("#NEWLINE#".join(self.users_error_check_list).replace("#NEWLINE#", "\n\n")), self.thread_id_results), public=False, brand=self.brand):
                                        self.zen_return = self.module_zen.search_id(self.ticket_id_results, brand=self.brand)
                                        time.sleep(3)
                                        if self.zen_return is not False:
                                            self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search)
                                            self.zen_return.assignee = None
                                            self.zen_return.status = "open"
                                            self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                            self.module_database.update_analyzing("end_ticket", 2, self.thread_id_results)
                                            self._log.info("Completed ticket - {} - {}".format(self.ticket_id_results, self.user_results))
                                    else:
                                        self._log.error("Comment completed ticket failed - {} - {}".format(self.ticket_id_results, self.user_results))

                    except Exception as er:
                        # generate a error log
                        self._log.error("for result_check - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id))
                        continue

        except Exception as er:
            # generate a error log
            self._log.error("apply_results - {} - {}".format(__name__, er))
            self.general_error = True
            return False

    def process_database(self):
        try:
            self.vars_ansible = None
            self.summary_ansible = False
            # Get database migrations
            self.result_register = self.module_database.get_register_migrations()
            if self.result_register is not None and self.result_register is not False and len(self.result_register) > 0:
                # walks the tickets
                for self.line_register in self.result_register:
                    try:
                        # clean variables
                        self.clean_variables()
                        # set false for item used in checking
                        self.general_error = False
                        self.check_message = False
                        # generate threadID
                        self.thread_id = str(uuid.uuid4())
                        # set values
                        self.set_values(self.line_register)
                        self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                        self.module_database.update_analyzing("thread_id", self.thread_id, ticket_id=self.ticket_id, main_domain=self.main_domain)
                        if self.zen_return is not False:
                            self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                            self.request_type = self.module_regex.check_request_type(self.zen_return.subject)
                            # call function to check and get data in ticket
                            if self.check_type():
                                if self.all_users == 0 and (self.src_type == "vps" or self.src_type == "dedi"):
                                    if self.request_type is not False:
                                        self.vars_ansible = {
                                            "domain": self.main_domain,
                                            "ticketID": self.ticket_id,
                                            "threadID": self.thread_id,
                                            "type": "source",
                                            "src_type": self.src_type,
                                            "dst_type": self.dst_type,
                                        }
                                        if self.connect_ip == 1 and self.src_ip is not None:
                                            self.server = self.src_ip
                                        else:
                                            self.server = self.src_server
                                        if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain, source_database=True):
                                            self.apply_migration(brand=self.brand)
                                            self.handle_info(brand=self.brand)
                                        else:
                                            self.general_error = True
                                            self.apply_duplicated(brand=self.brand)
                                        if not self.general_error:
                                            if self.specific_migration == 0:
                                                self.file_flag_account_suspended = os.path.join(self.report_casepath, "account_suspended.flag")
                                                if os.path.exists(self.file_flag_account_suspended):
                                                    os.remove(self.file_flag_account_suspended)
                                                self.module_database.update_analyzing("check_source", 1, self.thread_id)
                                                self.module_database.update_analyzing("all_users", 1, self.thread_id)
                                                self.module_database.update_analyzing("status", 1, self.thread_id)
                                                self._log.debug("Allusers check_source - {} - {}".format(self.vars_ansible, self.server))
                                                self.summary_ansible = self.module_ansible.execute(self.playbook_check, self.vars_ansible, self.server)
                                                if self.summary_ansible is False or self.summary_ansible is None:
                                                    # update check type with failed
                                                    self.module_database.update_analyzing("check_source", 2, self.thread_id)
                                                    self.module_database.update_analyzing("all_users", 2, self.thread_id)
                                                    self.module_database.update_analyzing("status", 2, self.thread_id)
                                                    self.vars_ansible = None
                                                    self.summary_ansible = False
                                                    self.general_error = True
                                                    # error log
                                                    self._log.error("Allusers ansible check failed - {} - {}".format(self.main_domain, self.thread_id))
                                                    if os.path.exists(os.path.join(self.report_casepath, "account_suspended.flag")):
                                                        self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Error because account is suspended, require unsuspend.", self.thread_id),
                                                                                       public=False, brand=self.brand)
                                                    else:
                                                        self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Error in allusers ansible check", self.thread_id),
                                                                                       public=False, brand=self.brand)
                                                else:
                                                    self.summary_ansible = False
                                                    self.vars_ansible = None
                                                    self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                                                    self.file_domain_user_data = os.path.join(self.report_casepath, "source/domainUserData.json")
                                                    if os.path.exists(self.file_domain_user_data):
                                                        try:
                                                            with closing(open(self.file_domain_user_data)) as self.open_domain_user_data:
                                                                self.result_domain_user_data = json.load(self.open_domain_user_data)
                                                                if int(self.result_domain_user_data['metadata']['result']) == 1:
                                                                    self.user = self.result_domain_user_data['data']['userdata']['user']
                                                                    self.home = self.result_domain_user_data['data']['userdata']['homedir']
                                                                    if self.user is not None and self.user is not False and self.home is not None and self.home is not False:
                                                                        self.module_database.update_analyzing("user", self.user, self.thread_id)
                                                                        self.module_database.update_analyzing("home", self.home, self.thread_id)
                                                                        self.module_database.update_analyzing("check_source", 3, self.thread_id)
                                                                        self.module_database.update_analyzing("all_users", 3, self.thread_id)
                                                                        self._log.debug("Allusers ansible check completed - {} - {}".format(self.main_domain, self.thread_id))
                                                                    else:
                                                                        self._log.error("Failed get user / home in json - {}".format(self.ticket_id))
                                                                        self.module_database.update_analyzing("check_source", 2, self.thread_id)
                                                                        self.module_database.update_analyzing("status", 2, self.thread_id)
                                                                        self.module_database.update_analyzing("all_users", 2, self.thread_id)
                                                                        self.general_error = True
                                                                        self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Error get user / home in allusers check", self.thread_id),
                                                                                                       public=False, brand=self.brand)

                                                        except Exception as er:
                                                            self.general_error = True
                                                            self._log.error("Failed handled user / home in json - {}".format(self.ticket_id, er))
                                                            self.module_database.update_analyzing("check_source", 2, self.thread_id)
                                                            self.module_database.update_analyzing("status", 2, self.thread_id)
                                                            self.module_database.update_analyzing("all_users", 2, self.thread_id)
                                                            self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Error exception get user / home in allusers check", self.thread_id),
                                                                                           public=False, brand=self.brand)
                                                    else:
                                                        self.general_error = True
                                                        self._log.error("domainUserData.json not found - {}".format(self.ticket_id))
                                                        self.module_database.update_analyzing("check_source", 2, self.thread_id)
                                                        self.module_database.update_analyzing("status", 2, self.thread_id)
                                                        self.module_database.update_analyzing("all_users", 2, self.thread_id)
                                                        self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Error JSON not found in allusers check", self.thread_id),
                                                                                       public=False, brand=self.brand)
                                            elif self.specific_migration == 1 and len(self.list_migration) > 0:
                                                self.module_database.update_analyzing("check_source", 3, self.thread_id)
                                                self.module_database.update_analyzing("all_users", 3, self.thread_id)
                                            else:
                                                self._log.info("Invalid specific_migration - {}".format(self.ticket_id))
                                    else:
                                        self._log.info("Invalid request_type - {}".format(self.ticket_id))
                                        self.general_error = True
                                else:
                                    if self.check_ns() or self.force_ns == 1:
                                        if self.request_type is not False:
                                            if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain, source_database=True):
                                                self.apply_migration(brand=self.brand)
                                                self.handle_info(brand=self.brand)
                                            else:
                                                self.apply_duplicated(brand=self.brand)
                                        else:
                                            self._log.info("Invalid request_type - {}".format(self.ticket_id))
                                            self.general_error = True
                                        if not self.general_error:
                                            self.message_manager()
                                            if self.check_message and not self.general_error:
                                                self._log.info("Finish apply_migration type - {} in '{}'".format(self.request_type, self.ticket_id))
                                    else:
                                        self.apply_send_queue("NS", brand=self.brand)

                        # check error in handled
                        if self.general_error:
                            self.apply_error(brand=self.brand)
                            self._log.info("Finish apply_error in - '{}'".format(self.ticket_id))
                            continue

                    except Exception as er:
                        # generate a error log
                        self._log.error("for result_register - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id))
                        continue

            # Get owners completed migration
            self.result_owners = self.module_database.get_owners_completed()
            if self.result_owners is not None and self.result_owners is not False and len(self.result_owners) > 0:
                # walks the tickets
                for self.line_owner in self.result_owners:
                    try:
                        self.ticket_id_owner = None
                        # set values
                        self.general_error_owner = False
                        self.src_server_owner = self.line_owner[0]
                        self.dst_server_owner = self.line_owner[1]
                        self.main_domain_owner = self.line_owner[2]
                        self.ticket_id_owner = int(self.line_owner[3])
                        self.force_ns_owner = int(self.line_owner[4])
                        self.specific_migration_owner = int(self.line_owner[5])
                        self.thread_id_owner = self.line_owner[6]
                        self.list_migration_owner = self.line_owner[7]
                        self.user_owner = self.line_owner[8]
                        self.dst_ip_owner = self.line_owner[9]
                        self.src_ip_owner = self.line_owner[10]
                        self.connect_ip_owner = self.line_owner[11]
                        self.brand_owner = self.line_owner[12]
                        self.result_clients = None
                        self.info_list = list()
                        self.info_list.append(self.thread_id_owner)
                        self.info_list.append(self.main_domain_owner)
                        self.info_list.append(self.user_owner)
                        self.module_zen.comment_ticket(self.ticket_id_owner, self.module_templates.info_completed(self.info_list, this_owner=True), public=False, brand=self.brand_owner)
                        self.module_database.update_analyzing("check_clients", 1, self.thread_id_owner)
                        if self.specific_migration_owner == 0:
                            self.report_casepath = os.path.join(self.report_dir, str(self.main_domain_owner) + "_" + str(self.ticket_id_owner) + "_" + str(self.thread_id_owner))
                            self.file_reseller_accounts_data = os.path.join(self.report_casepath, "source/reseller_accounts_data.json")
                            if os.path.exists(self.file_reseller_accounts_data):
                                with closing(open(self.file_reseller_accounts_data)) as self.open_reseller_accounts_data:
                                    self.result_reseller_accounts_data = json.load(self.open_reseller_accounts_data)
                                    if self.result_reseller_accounts_data['metadata']['result'] == 1 and self.result_reseller_accounts_data['metadata']['reason'] == "OK":
                                        self.result_clients = self.result_reseller_accounts_data['data']['reseller']['acct']
                        elif self.specific_migration_owner == 1:
                            if self.list_migration_owner is not None and self.list_migration_owner is not False:
                                if "," in self.list_migration_owner:
                                    self.result_clients = self.list_migration_owner.split(",")
                                else:
                                    self.result_clients = list()
                                    self.result_clients.append(self.list_migration_owner)
                                self.module_database.update_analyzing("count_specific_migration", len(self.result_clients) + 1, self.thread_id_owner)
                        if self.result_clients is not None:
                            for self.reseller_account in self.result_clients:
                                try:
                                    self.clean_variables()
                                    # set false for item used in checking
                                    self.general_error = False
                                    self.check_message = False
                                    # generate threadID
                                    self.thread_id = str(uuid.uuid4())
                                    if self.specific_migration_owner == 0:
                                        self.main_domain = self.reseller_account['domain']
                                    elif self.specific_migration_owner == 1:
                                        self.main_domain = self.reseller_account
                                    self.ticket_id = self.ticket_id_owner
                                    self.src_server = self.src_server_owner
                                    self.dst_server = self.dst_server_owner
                                    self.force_ns = self.force_ns_owner
                                    self.zen_return = self.module_zen.search_id(self.ticket_id_owner, brand=self.brand_owner)
                                    if self.main_domain != self.main_domain_owner:
                                        if self.zen_return is not False:
                                            self.request_type = self.module_regex.check_request_type(self.zen_return.subject)
                                            # call function to check and get data in ticket
                                            self.src_type = "shared"
                                            self.dst_type = "shared"
                                            if self.check_ns() or self.force_ns == 1:
                                                if self.request_type is not False:
                                                    if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain):
                                                        self.apply_database_client()
                                                        if not self.general_error:
                                                            self.handle_info(brand=self.brand_owner)
                                                    else:
                                                        self.general_error = True
                                                        self.apply_duplicated(brand=self.brand_owner)
                                                else:
                                                    self._log.info("Invalid client request_type - {} - {}".format(self.ticket_id_owner, self.main_domain))
                                                    self.general_error = True
                                                if not self.general_error:
                                                    self.message_manager()
                                                    if self.check_message and not self.general_error:
                                                        self._log.info("Finish migration client - {} in '{}'".format(self.main_domain, self.ticket_id_owner))
                                            else:
                                                self.apply_send_queue("NS", brand=self.brand_owner)

                                    if not self.general_error_owner:
                                        self.general_error_owner = self.general_error

                                    # check error in handled
                                    if self.general_error:
                                        self.module_zen.comment_ticket(self.ticket_id_owner, self.module_zen.comment_error("Error in client migration", self.reseller_account), public=False, brand=self.brand_owner)
                                        self._log.info("Finish error in client migration in - '{}' - '{}'".format(self.ticket_id_owner, self.reseller_account))

                                except Exception as er:
                                    self._log.error("process_tickets - '{}' - '{}' - '{}'".format(__name__, er, self.reseller_account))
                                    continue

                        if self.general_error_owner:
                            self.module_database.update_analyzing("check_clients", 2, self.thread_id_owner)
                        else:
                            self.module_database.update_analyzing("check_clients", 3, self.thread_id_owner)

                    except Exception as er:
                        self.module_database.update_analyzing("check_clients", 2, self.thread_id_owner)
                        # generate a error log
                        self._log.error("for result_owners - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id_owner))
                        continue

            # Get owners completed migration
            self.result_allusers = self.module_database.get_allusers_completed()
            if self.result_allusers is not None and self.result_allusers is not False and len(self.result_allusers) > 0:
                # walks the tickets
                for self.line_allusers in self.result_allusers:
                    try:
                        self.general_error_allusers = False
                        self.ticket_id_allusers = None
                        # set values
                        self.src_server_allusers = self.line_allusers[0]
                        self.dst_server_allusers = self.line_allusers[1]
                        self.main_domain_allusers = self.line_allusers[2]
                        self.ticket_id_allusers = int(self.line_allusers[3])
                        self.force_ns_allusers = int(self.line_allusers[4])
                        self.specific_migration_allusers = int(self.line_allusers[5])
                        self.thread_id_allusers = self.line_allusers[6]
                        self.list_migration_allusers = self.line_allusers[7]
                        self.dst_ip_allusers = self.line_allusers[8]
                        self.src_ip_allusers = self.line_allusers[9]
                        self.connect_ip_allusers = self.line_allusers[10]
                        self.brand_allusers = self.line_allusers[11]
                        self.result_allusers = None
                        self.module_database.update_analyzing("check_allusers", 1, self.thread_id_allusers)
                        if self.specific_migration_allusers == 0:
                            self.report_casepath = os.path.join(self.report_dir, str(self.main_domain_allusers) + "_" + str(self.ticket_id_allusers) + "_" + str(self.thread_id_allusers))
                            self.file_allusers_accounts_data = os.path.join(self.report_casepath, "source/list_accts.json")
                            if os.path.exists(self.file_allusers_accounts_data):
                                with closing(open(self.file_allusers_accounts_data)) as self.open_allusers_accounts_data:
                                    self.result_allusers_accounts_data = json.load(self.open_allusers_accounts_data)
                                    if self.result_allusers_accounts_data['metadata']['result'] == 1 and self.result_allusers_accounts_data['metadata']['reason'] == "OK":
                                        self.result_allusers = self.result_allusers_accounts_data['data']['acct']
                        elif self.specific_migration_allusers == 1:
                            if self.list_migration_allusers is not None and self.list_migration_allusers is not False:
                                if "," in self.list_migration_allusers:
                                    self.result_allusers = self.list_migration_allusers.split(",")
                                else:
                                    self.result_allusers = list()
                                    self.result_allusers.append(self.list_migration_allusers)
                                self.module_database.update_analyzing("count_specific_migration", len(self.result_allusers), self.thread_id_allusers)
                        if self.result_allusers is not None:
                            for self.allusers_account in self.result_allusers:
                                try:
                                    self.clean_variables()
                                    # set false for item used in checking
                                    self.general_error = False
                                    self.check_message = False
                                    if self.specific_migration_allusers == 0:
                                        self.main_domain = self.allusers_account['domain']
                                    elif self.specific_migration_allusers == 1:
                                        self.main_domain = self.allusers_account
                                    if self.main_domain == self.main_domain_allusers:
                                        self.thread_id = self.thread_id_allusers
                                    else:
                                        self.thread_id = str(uuid.uuid4())
                                    self.ticket_id = self.ticket_id_allusers
                                    self.src_server = self.src_server_allusers
                                    self.dst_server = self.dst_server_allusers
                                    self.force_ns = self.force_ns_allusers
                                    if self.main_domain == self.main_domain_allusers and self.specific_migration_allusers == 0:
                                        self.message_manager(main_account=True)
                                    elif self.main_domain == self.main_domain_allusers and self.specific_migration_allusers == 1:
                                        self.module_database.update_analyzing("check_source", 0, self.thread_id_allusers)
                                        self.message_manager()
                                    else:
                                        self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand_allusers)
                                        if self.zen_return is not False:
                                            self.request_type = self.module_regex.check_request_type(self.zen_return.subject)
                                            # call function to check and get data in ticket
                                            if self.check_type():
                                                if self.check_ns() or self.force_ns == 1:
                                                    if self.request_type is not False:
                                                        if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain):
                                                            self.apply_database_allusers()
                                                            if not self.general_error:
                                                                self.handle_info(brand=self.brand_allusers)
                                                        else:
                                                            self.general_error = True
                                                            self.apply_duplicated(brand=self.brand_allusers)
                                                    else:
                                                        self._log.info("Invalid allusers request_type - {} - {}".format(self.ticket_id, self.main_domain))
                                                        self.general_error = True
                                                    if not self.general_error:
                                                        self.message_manager()
                                                        if self.check_message and not self.general_error:
                                                            self._log.info("Finish migration allusers - {} in '{}'".format(self.main_domain, self.ticket_id))
                                                else:
                                                    self.apply_send_queue("NS", brand=self.brand_allusers)

                                    if not self.general_error_allusers:
                                        self.general_error_allusers = self.general_error

                                    # check error in handled
                                    if self.general_error:
                                        self.module_zen.comment_ticket(self.ticket_id_allusers, self.module_zen.comment_error("Error in user migration", self.thread_id_allusers), public=False, brand=self.brand_allusers)
                                        self._log.info("Finish error in user migration in - '{}' - '{}'".format(self.ticket_id_allusers, self.allusers_account))

                                except Exception as er:
                                    self._log.error("process_tickets - '{}' - '{}' - '{}'".format(__name__, er, self.allusers_account))
                                    continue
                        else:
                            self.general_error_allusers = True

                        if self.general_error_allusers:
                            self.module_database.update_analyzing("check_allusers", 2, self.thread_id_allusers)
                        else:
                            self.module_database.update_analyzing("check_allusers", 3, self.thread_id_allusers)

                    except Exception as er:
                        self.module_database.update_analyzing("check_allusers", 2, self.thread_id_allusers)
                        # generate a error log
                        self._log.error("for result_allusers - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id_allusers))
                        continue

        except Exception as er:
            # generate a error log
            self._log.critical("{} - {}".format(__name__, er))
            return False
