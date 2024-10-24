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
import uuid
import time


class ModuleZencheck:

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
            # variables
            self._log = self.module_log.log
            self.request_type = None
            self.ns_server = None
            self.zen_return = None
            self.message = None
            self.info_list = list()
            self.tickets_object = None
            self.main_domain = None
            self.tickets_result = None
            self.tickets_json = None
            self.ticket = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.migration_data = None
            self.list_data = None
            self.type_problem = None
            self.brand = None
            self.queue_manager = ModulePublish(self._log, "manager", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                               self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("manager"))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            # exit the application with code 4
            exit(4)

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
                self.module_log = ModuleLog(self.module_configuration, 1)
                if self.module_log is not None and not self.module_log.initialize():
                    print("Error in initialize ModuleLog")
                    return False
                else:
                    return True

        except Exception as er:
            # only print the error, since ModuleLog there isn't instance
            print("{} - {}".format(__name__, er))
            return False

    def message_manager(self):
        try:
            self.message = dict()
            self.message.update({'sender': 'zencheck'})
            self.message.update({'id': self.ticket['id']})
            self.message.update({'thread_id': self.ticket['thread_id']})
            self.queue_manager.publish(self.message)
            self._log.info("Send manager {}".format(self.message))
            self.ticket.update({'check_message': True})

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            self.ticket.update({"general_error": True})
            return False

    def check_type(self):
        try:
            self.src_type = self.module_regex.check_type(self.src_server)
            self.dst_type = self.module_regex.check_type(self.dst_server)
            if self.src_type is not False and self.dst_type is not False:
                return True
            else:
                self._log.error("check_type failed in src_type or dst_type")
                self.ticket.update({"general_error": True})
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            self.ticket.update({"general_error": True})
            return False

    def check_ticket(self):
        try:
            self.list_data = self.module_regex.get_data(self.ticket['description'])
            if self.list_data is not False and len(self.list_data) == 3:
                self.main_domain = self.list_data[0]
                self.src_server = self.list_data[1]
                self.dst_server = self.list_data[2]
                return True
            else:
                self._log.error("check_ticket failed in list_data")
                self.ticket.update({"general_error": True})
                return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            self.ticket.update({"general_error": True})
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
            self.ticket.update({"general_error": True})
            return False

    def apply_error(self, brand="br"):
        try:
            self.brand = brand
            # comment in ticket
            self.module_zen.comment_ticket(self.ticket['id'], self.module_zen.comment_error("Apply error", self.ticket['thread_id']), public=False, brand=self.brand)
            # get ticket object
            self.zen_return = self.module_zen.search_id(self.ticket['id'], brand=self.brand)
            if self.zen_return is not False:
                if self.module_database.check_thread_id(self.ticket['thread_id']):
                    # update status analyzing
                    self.module_database.update_analyzing("status", 2, thread_id=self.ticket['thread_id'])
                    # update analyzing
                    self.module_database.update_analyzing("handled", 0, thread_id=self.ticket['thread_id'])
                else:
                    if self.module_database.insert_analyzing(self.ticket['id'], thread_id=self.ticket['thread_id'], brand=self.brand):
                        # update status analyzing
                        self.module_database.update_analyzing("status", 2, thread_id=self.ticket['thread_id'])
                        # update analyzing
                        self.module_database.update_analyzing("handled", 0, thread_id=self.ticket['thread_id'])
                    else:
                        self._log.error("insert in apply_error - '{}'".format(self.ticket['id']))
                # update ticket
                self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search)
                self.zen_return.assignee = None
                self.zen_return.status = "open"
                # apply the change in ticket
                self.module_zen.update_ticket(self.zen_return)
                # generate a info log
                self._log.info("apply_error in - '{}'".format(self.ticket['id']))

        except Exception as er:
            # generate a error log
            self._log.error("apply_error - {} - {} - {}".format(__name__, er, self.ticket['id']))
            return False

    def apply_send_queue(self, type_problem, brand="br"):
        try:
            self.brand = brand
            self.type_problem = type_problem
            if self.type_problem == "NS":
                # comment in ticket
                self.module_zen.comment_ticket(self.ticket['id'], self.module_zen.comment_error("Not using NS to shared server."
                                                                                                "\n\nIn the event of a positive customer response, you only need to put the ticket on hold."
                                                                                                "\n\nNS1: {}".format(self.ns_server), self.ticket['thread_id']), public=False, brand=self.brand)
                time.sleep(3)
                if self.ns_server is not False:
                    self.module_zen.comment_ticket(self.ticket['id'], self.module_templates.not_ns(brand=self.brand))
                time.sleep(3)
            # get ticket object
            self.zen_return = self.module_zen.search_id(self.ticket['id'], brand=self.brand)
            if self.zen_return is not False:
                # update ticket
                self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_ns_not)
                self.zen_return.assignee = None
                self.zen_return.priority = "high"
                self.zen_return.status = "pending"
                # apply the change in ticket
                self.module_zen.update_ticket(self.zen_return)
                # generate a info log
                self._log.info("apply_send_queue in - '{}'".format(self.ticket['id']))

        except Exception as er:
            # generate a error log
            self._log.error("apply_send_queue - {} - {} - {}".format(__name__, er, self.ticket['id']))
            return False

    def apply_database(self, brand="br"):
        try:
            self.brand = brand
            if self.module_database.check_thread_id(self.ticket['thread_id']):
                # update analyzing
                self.module_database.update_analyzing("status", 1, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("request_type", self.request_type, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("handled", 1, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("src_server", self.src_server, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("dst_server", self.dst_server, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("src_type", self.src_type, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("dst_type", self.dst_type, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("main_domain", self.main_domain, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("ticket_id", self.ticket['id'], thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("register_type", 1, thread_id=self.ticket['thread_id'])
                self.module_database.update_analyzing("brand", self.brand, thread_id=self.ticket['thread_id'])
            else:
                if self.module_database.insert_analyzing(self.ticket['id'], thread_id=self.ticket['thread_id'], brand=self.brand):
                    self.module_database.update_analyzing("status", 1, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("request_type", self.request_type, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("handled", 1, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("src_server", self.src_server, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("dst_server", self.dst_server, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("src_type", self.src_type, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("dst_type", self.dst_type, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("main_domain", self.main_domain, thread_id=self.ticket['thread_id'])
                    self.module_database.update_analyzing("register_type", 1, thread_id=self.ticket['thread_id'])
                else:
                    self._log.error("insert in apply_database - '{}'".format(self.ticket['id']))
                    self.ticket.update({"general_error": True})

        except Exception as er:
            # generate a error log
            self._log.error("apply_database - {} - {} - {}".format(__name__, er, self.ticket['id']))
            self.ticket.update({"general_error": True})
            return False

    def handle_info(self, brand="br"):
        try:
            self.brand = brand
            self.info_list = list()
            self.info_list.append(self.ticket['thread_id'])
            self.info_list.append(self.src_type)
            self.info_list.append(self.src_server)
            self.info_list.append(self.dst_type)
            self.info_list.append(self.dst_server)
            self.info_list.append(self.main_domain)
            self.info_list.append(self.request_type)
            self.module_zen.comment_ticket(self.ticket['id'], self.module_templates.info_started(self.info_list), public=False, brand=self.brand)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("handle_info - {} - {} - {}".format(__name__, er, self.ticket['id']))
            return False

    def apply_duplicated(self, brand="br"):
        try:
            self.brand = brand
            # comment in ticket
            # self.zen_return = self.module_zen.macro(self.ticket['id'], self.module_zen.macro_start_id)
            if self.module_zen.comment_ticket(self.ticket['id'], self.module_zen.comment_error("Migration duplicated", self.main_domain), public=False, brand=self.brand):
                if not self.ticket['general_error']:
                    self.zen_return = self.module_zen.search_id(self.ticket['id'], brand=self.brand)
                    if self.zen_return is not False:
                        # update ticket
                        self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search)
                        self.zen_return.status = "open"
                        # apply the change in ticket
                        self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                        # generate a info log
                        self._log.info("apply_duplicated in - '{}'".format(self.ticket['id']))
            else:
                self._log.error("Comment duplicated ticket failed in apply_duplicated - {} - {}".format(self.ticket['id'], self.main_domain))

        except Exception as er:
            # generate a error log
            self._log.error("apply_duplicated - {} - {} - {}".format(__name__, er, self.ticket['id']))
            self.ticket.update({"general_error": True})
            return False

    def apply_migration_turbo(self, brand="br"):
        try:
            self.brand = brand
            # comment in ticket
            # self.zen_return = self.module_zen.macro(self.ticket['id'], self.module_zen.macro_start_id)
            if self.module_zen.comment_ticket(self.ticket['id'], self.module_templates.turbo_started(brand=self.brand), brand=self.brand):
                if not self.ticket['general_error']:
                    self.zen_return = self.module_zen.search_id(self.ticket['id'], brand=self.brand)
                    if self.zen_return is not False:
                        # update ticket
                        self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_handled, self.module_zen.tag_search)
                        self.zen_return.status = "pending"
                        # apply the change in ticket
                        if self.module_zen.update_ticket(self.zen_return, brand=self.brand) is not False:
                            self.apply_database()
                            # generate a info log
                            self._log.info("apply_migration_turbo in - '{}'".format(self.ticket['id']))
            else:
                self._log.error("Comment started ticket failed in apply_migration_turbo - {} - {}".format(self.ticket['id'], self.ticket['thread_id']))

        except Exception as er:
            # generate a error log
            self._log.error("apply_migration_turbo - {} - {} - {}".format(__name__, er, self.ticket['id']))
            self.ticket.update({"general_error": True})
            return False

    def apply_migration_monitoring(self, brand="br"):
        try:
            self.brand = brand
            # comment in ticket
            # self.zen_return = self.module_zen.macro(self.ticket['id'], self.module_zen.macro_start_id)
            if self.module_zen.comment_ticket(self.ticket['id'], self.module_templates.monitoring_started(brand=self.brand), brand=self.brand):
                if not self.ticket['general_error']:
                    self.zen_return = self.module_zen.search_id(self.ticket['id'], brand=self.brand)
                    if self.zen_return is not False:
                        # update ticket
                        self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_handled, self.module_zen.tag_search)
                        self.zen_return.status = "pending"
                        # apply the change in ticket
                        if self.module_zen.update_ticket(self.zen_return, brand=self.brand) is not False:
                            self.apply_database()
                            # generate a info log
                            self._log.info("apply_migration_monitoring in - '{}'".format(self.ticket['id']))
            else:
                self._log.error("Comment started ticket failed in apply_migration_monitoring - {} - {}".format(self.ticket['id'], self.ticket['thread_id']))

        except Exception as er:
            # generate a error log
            self._log.error("apply_migration_monitoring - {} - {} - {}".format(__name__, er, self.ticket['id']))
            self.ticket.update({"general_error": True})
            return False

    def process_tickets(self):
        try:
            self.tickets_result = None
            # Get gold tickets in migration group with tag not_checked
            self.tickets_object = self.module_zen.search_migration()
            if self.tickets_object is not False:
                self.tickets_json = self.tickets_object._response_json
                self.tickets_result = self.tickets_json.get('results')
            if self.tickets_result is not None and len(self.tickets_result) > 0:
                # walks the tickets
                for self.ticket in self.tickets_result:
                    try:
                        # set false for item used in checking
                        self.ticket.update({'general_error': False})
                        self.ticket.update({'check_message': False})
                        # generate threadID
                        self.ticket.update({'thread_id': str(uuid.uuid4())})
                        # call function to check and get data in ticket
                        if self.check_ticket() and self.check_type():
                            if "sh-pro" in self.src_server and "sh-pro" in self.dst_server:
                                self.ticket.update({"general_error": True})
                                self.module_zen.comment_ticket(self.ticket['id'], self.module_zen.comment_error("Source server and Destination server is sh-pro, require checking.", self.ticket['id']), public=False)
                            elif self.check_ns() or self.module_zen.tag_force_ns in self.ticket['tags']:
                                self.request_type = self.module_regex.check_request_type(self.ticket['subject'])
                                if self.request_type is not False and self.request_type == 1:
                                    if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain):
                                        self.apply_migration_turbo()
                                        if not self.ticket['general_error']:
                                            self.handle_info()
                                    else:
                                        self.apply_duplicated()
                                elif self.request_type is not False and self.request_type == 2:
                                    if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain):
                                        self.apply_migration_monitoring()
                                        if not self.ticket['general_error']:
                                            self.handle_info()
                                    else:
                                        self.apply_duplicated()
                                else:
                                    self._log.info("Invalid request_type - {}".format(self.ticket['id']))
                                    self.ticket.update({'general_error': True})
                                if not self.ticket['general_error']:
                                    self.message_manager()
                                    if self.ticket['check_message'] and not self.ticket['general_error']:
                                        self._log.info("Finish apply_migration type - {} in '{}'".format(self.request_type, self.ticket['id']))
                            else:
                                self.apply_send_queue("NS")
                        # check error in handled
                        if self.ticket['general_error']:
                            self.apply_error()
                            self._log.info("Finish apply_error in - '{}'".format(self.ticket['id']))
                            continue

                    except Exception as er:
                        # generate a error log
                        self._log.error("for tickets_result - '{}' - '{}' - '{}'".format(__name__, er, self.ticket))
                        continue

            # generate a info log
            self._log.info("Entering in sleep - 10 minutes")

        except Exception as er:
            # generate a error log
            self._log.critical("{} - {}".format(__name__, er))
            return False

    def process_tickets_es(self):
        try:
            self.tickets_result = None
            # Get gold tickets in migration group with tag not_checked
            self.tickets_object = self.module_zen.search_migration(brand="es")
            if self.tickets_object is not False:
                self.tickets_json = self.tickets_object._response_json
                self.tickets_result = self.tickets_json.get('results')
            if self.tickets_result is not None and len(self.tickets_result) > 0:
                # walks the tickets
                for self.ticket in self.tickets_result:
                    try:
                        # set false for item used in checking
                        self.ticket.update({'general_error': False})
                        self.ticket.update({'check_message': False})
                        # generate threadID
                        self.ticket.update({'thread_id': str(uuid.uuid4())})
                        # call function to check and get data in ticket
                        if self.check_ticket() and self.check_type():
                            if "sh-pro" in self.src_server and "sh-pro" in self.dst_server:
                                self.ticket.update({"general_error": True})
                                self.module_zen.comment_ticket(self.ticket['id'], self.module_zen.comment_error("Source server and Destination server is sh-pro, require checking.", self.ticket['id']), public=False, brand="es")
                            elif self.check_ns() or self.module_zen.tag_force_ns in self.ticket['tags']:
                                self.request_type = self.module_regex.check_request_type(self.ticket['subject'])
                                if self.request_type is not False and self.request_type == 1:
                                    if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain):
                                        self.apply_migration_turbo(brand="es")
                                        if not self.ticket['general_error']:
                                            self.handle_info(brand="es")
                                    else:
                                        self.apply_duplicated(brand="es")
                                elif self.request_type is not False and self.request_type == 2:
                                    if self.module_database.check_duplicated(self.src_server, self.dst_server, self.main_domain):
                                        self.apply_migration_monitoring(brand="es")
                                        if not self.ticket['general_error']:
                                            self.handle_info(brand="es")
                                    else:
                                        self.apply_duplicated(brand="es")
                                else:
                                    self._log.info("Invalid request_type - {}".format(self.ticket['id']))
                                    self.ticket.update({'general_error': True})
                                if not self.ticket['general_error']:
                                    self.message_manager()
                                    if self.ticket['check_message'] and not self.ticket['general_error']:
                                        self._log.info("Finish apply_migration type - {} in '{}'".format(self.request_type, self.ticket['id']))
                            else:
                                self.apply_send_queue("NS", brand="es")
                        # check error in handled
                        if self.ticket['general_error']:
                            self.apply_error(brand="es")
                            self._log.info("Finish apply_error in - '{}'".format(self.ticket['id']))
                            continue

                    except Exception as er:
                        # generate a error log
                        self._log.error("for tickets_result - '{}' - '{}' - '{}'".format(__name__, er, self.ticket))
                        continue

            # generate a info log
            self._log.info("Entering in sleep - 10 minutes")

        except Exception as er:
            # generate a error log
            self._log.critical("{} - {}".format(__name__, er))
            return False
