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
from migration_automation_manager.module_configuration import ModuleConfiguration
from migration_automation_manager.module_publish import ModulePublish
from migration_automation_manager.module_database import ModuleDatabase
import time


class ModuleRetry:

    def __init__(self, development=None):
        try:
            self.development = development
            self.module_configuration = None
            self.module_log = None
            # load the conf
            if not self.config_init():
                exit(3)
            # instance of the modules
            self.module_zen = ModuleZen(self.module_log.log, self.module_configuration)
            self.module_database = ModuleDatabase(self.module_log.log, self.module_configuration)
            # variables
            self._log = self.module_log.log
            self.tickets_object = None
            self.ticket_id = None
            self.available_user = None
            self.tickets_json = None
            self.tickets_result = None
            self.check_destination_end = None
            self.check_destination = None
            self.check_source = None
            self.mysql_dump = None
            self.mysql_restore = None
            self.cpanel_restore = None
            self.cpanel_pkgacct = None
            self.compare = None
            self.suspend = None
            self.remove = None
            self.rsync = None
            self.rsync_last = None
            self.values_database = None
            self.message = None
            self.sender = None
            self.thread_id = None
            self.handle_dns_source = None
            self.handle_dns_destination_end = None
            self.status = None
            self.zen_return = None
            self.result_retry = None
            self.db_retry = None
            self.value_retry = None
            self.retry = None
            self.brand = None
            self.client = None
            self.end_tasks = None
            self.brand_tickets = None
            self.thread_id_main = None
            self.end_ticket_main = None
            self.register_type = None
            self.all_users = None
            self.not_send_message = False
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
                self.module_log = ModuleLog(self.module_configuration, 13)
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
            self.message.update({'sender': self.sender})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            if self.available_user is True:
                self.message.update({'available_user': self.available_user})
            self._log.info("Send message to manager - {}".format(self.message))
            self.queue_manager.publish(self.message)
            self.available_user = None
            self.sender = None
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message manager - {} - {}".format(self.__class__.__name__, er))
            return False

    def check_register_type(self):
        try:
            if self.client is not None and self.client is not False and \
                    self.end_tasks is not None and self.end_tasks is not False and \
                    self.client == 2 and self.end_tasks == 1:
                self.module_database.update_analyzing("client", 1, self.thread_id)
                self.module_database.update_analyzing("end_tasks", 0, self.thread_id)
            self.end_ticket_main = self.module_database.get_values(self.ticket_id, self.thread_id_main, "retry_main")
            if self.end_ticket_main is not None and self.end_ticket_main is not False and \
                    len(self.end_ticket_main) == 1 and int(self.end_ticket_main[0]) == 2:
                self.module_database.update_analyzing("end_ticket", 0, self.thread_id_main)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("check_register_type - {} - {}".format(self.__class__.__name__, er))
            return False

    def found_error(self):
        try:
            if self.check_source == 2 and self.register_type != 2 and self.all_users == 0:
                if self.module_database.update_analyzing("check_source", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "zencheck"
                    self.not_send_message = False
                    return True
            elif self.check_source == 2 and self.register_type == 2 and self.all_users == 2 and self.check_destination == 0:
                if self.module_database.update_analyzing("check_source", 0, self.thread_id) and self.module_database.update_analyzing("status", 0, self.thread_id) and \
                        self.module_database.update_analyzing("all_users", 0, self.thread_id) and self.module_database.update_analyzing("handled", 1, self.thread_id):
                    self.not_send_message = True
                    return True
            elif self.check_destination == 2:
                if self.module_database.update_analyzing("check_destination", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "check"
                    self.not_send_message = False
                    return True
            elif self.cpanel_pkgacct == 2:
                if self.module_database.update_analyzing("cpanel_pkgacct", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "check"
                    self.not_send_message = False
                    return True
            elif self.cpanel_restore == 2:
                if self.module_database.update_analyzing("cpanel_restore", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "cpanel"
                    self.available_user = True
                    self.not_send_message = False
                    return True
            elif self.rsync == 2 and self.rsync_last == 0:
                if self.module_database.update_analyzing("rsync", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "cpanel"
                    self.not_send_message = False
                    return True
            elif self.check_destination_end == 2 and self.handle_dns_destination_end == 3 and self.handle_dns_source == 3 and self.rsync_last == 3:
                if self.module_database.update_analyzing("check_destination_end", 3, self.thread_id) and self.module_database.update_analyzing("status", 3, self.thread_id):
                    self.sender = "handle_account"
                    self.not_send_message = False
                    return True
            elif self.check_destination_end == 2 and self.handle_dns_destination_end == 0 and self.handle_dns_source == 0:
                if self.module_database.update_analyzing("check_destination_end", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "rsync"
                    self.not_send_message = False
                    return True
            elif self.compare == 2:
                if self.module_database.update_analyzing("compare", 0, self.thread_id) and self.module_database.update_analyzing("status", 3, self.thread_id):
                    self.sender = "rsync"
                    self.not_send_message = False
                    return True
            elif self.suspend == 2:
                if self.module_database.update_analyzing("suspend", 0, self.thread_id) and self.module_database.update_analyzing("status", 3, self.thread_id):
                    self.sender = "compare"
                    self.not_send_message = False
                    return True
            elif self.handle_dns_source == 2:
                if self.module_database.update_analyzing("handle_dns_source", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "check_end"
                    self.not_send_message = False
                    return True
            elif self.handle_dns_destination_end == 2:
                if self.module_database.update_analyzing("handle_dns_destination_end", 0, self.thread_id) and self.module_database.update_analyzing("status", 1, self.thread_id):
                    self.sender = "handle_dns"
                    self.not_send_message = False
                    return True
            elif self.rsync == 2 and self.rsync_last == 1:
                if self.module_database.update_analyzing("rsync_last", 0, self.thread_id) and self.module_database.update_analyzing("rsync", 3, self.thread_id) and self.module_database.update_analyzing("status", 3, self.thread_id):
                    self.sender = "handle_dns"
                    self.not_send_message = False
                    return True
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("found_error - {} - {} - {}".format(__name__, self.ticket_id, er))
            return False

    def process_tickets(self, brand="br"):
        try:
            self.brand_tickets = brand
            self.tickets_result = None
            # Get gold tickets in migration group with tag not_checked
            self.tickets_object = self.module_zen.search_migration_retry(brand=self.brand_tickets)
            if self.tickets_object is not False:
                self.tickets_json = self.tickets_object._response_json
                self.tickets_result = self.tickets_json.get('results')
            if self.tickets_result is not None and self.tickets_result is not False and len(self.tickets_result) > 0:
                # walks the tickets
                for self.ticket in self.tickets_result:
                    try:
                        self.ticket_id = self.ticket['id']
                        self.values_database = self.module_database.get_values(self.ticket_id, type_values="retry")
                        if self.values_database is not False and self.values_database is not None and len(self.values_database) == 1:
                            self.value_retry = self.values_database[0]
                            if len(self.value_retry) == 21:
                                self.check_source = int(self.value_retry[0])
                                self.check_destination = int(self.value_retry[1])
                                self.cpanel_pkgacct = int(self.value_retry[2])
                                self.cpanel_restore = int(self.value_retry[3])
                                self.brand = self.value_retry[4]
                                self.thread_id = self.value_retry[5]
                                self.rsync = int(self.value_retry[6])
                                self.retry = int(self.value_retry[7])
                                self.status = int(self.value_retry[8])
                                self.check_destination_end = int(self.value_retry[9])
                                self.compare = int(self.value_retry[10])
                                self.handle_dns_source = int(self.value_retry[11])
                                self.handle_dns_destination_end = int(self.value_retry[12])
                                self.rsync_last = int(self.value_retry[13])
                                self.suspend = int(self.value_retry[14])
                                self.remove = int(self.value_retry[15])
                                self.client = int(self.value_retry[16])
                                self.end_tasks = int(self.value_retry[17])
                                self.thread_id_main = self.value_retry[18]
                                self.register_type = int(self.value_retry[19])
                                self.all_users = int(self.value_retry[20])
                                if self.status == 2:
                                    if self.found_error():
                                        if not self.not_send_message:
                                            self.check_register_type()
                                            self.message_manager()
                                        self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                                        if self.zen_return is not False and self.zen_return is not None:
                                            # update ticket
                                            self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_handled, self.module_zen.tag_search_retry)
                                            self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_handled, self.module_zen.tag_error)
                                            self.zen_return.status = "pending"
                                            # apply the change in ticket
                                            self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                    else:
                                        self._log.info("not match in found_error - {} - {}".format(self.ticket_id, self.thread_id))
                                        self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Not match in found_error", self.thread_id), public=False, brand=self.brand)
                                        time.sleep(3)
                                        self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                                        if self.zen_return is not False and self.zen_return is not None:
                                            # update ticket
                                            self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search_retry)
                                            self.zen_return.status = "open"
                                            # apply the change in ticket
                                            self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                else:
                                    self._log.debug("status not error in ticket - {} - {}".format(self.ticket_id, self.thread_id))
                            else:
                                self._log.error("process_tickets retry failed in value retry check - '{}' - '{}'".format(__name__, self.ticket_id))
                        else:
                            self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                            if self.zen_return is not False and self.zen_return is not None:
                                # update ticket
                                self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_handled, self.module_zen.tag_search_retry)
                                self.zen_return.status = "open"
                                # apply the change in ticket
                                self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                            time.sleep(3)
                            self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Multiples accounts in ticket, require retry by front-end.", self.ticket_id), public=False, brand=self.brand)
                            self._log.info("process_tickets multiples accounts in ticket, require retry by front-end - '{}'".format(self.ticket_id))

                    except Exception as er:
                        # generate a error log
                        self._log.error("process_tickets retry - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id))
                        continue

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            return False

    def process_database(self):
        try:
            self.result_retry = None
            # Get gold tickets in migration group with tag not_checked
            self.result_retry = self.module_database.get_db_retry()
            if self.result_retry is not None and self.result_retry is not False and len(self.result_retry) > 0:
                # walks the tickets
                for self.db_retry in self.result_retry:
                    try:
                        self.ticket_id = self.db_retry[0]
                        self.values_database = self.module_database.get_values(self.ticket_id, type_values="retry")
                        if self.values_database is not False and self.values_database is not None and len(self.values_database) > 0:
                            for self.value_retry in self.values_database:
                                try:
                                    if len(self.value_retry) == 21:
                                        self.check_source = int(self.value_retry[0])
                                        self.check_destination = int(self.value_retry[1])
                                        self.cpanel_pkgacct = int(self.value_retry[2])
                                        self.cpanel_restore = int(self.value_retry[3])
                                        self.brand = self.value_retry[4]
                                        self.thread_id = self.value_retry[5]
                                        self.rsync = int(self.value_retry[6])
                                        self.retry = int(self.value_retry[7])
                                        self.status = int(self.value_retry[8])
                                        self.check_destination_end = int(self.value_retry[9])
                                        self.compare = int(self.value_retry[10])
                                        self.handle_dns_source = int(self.value_retry[11])
                                        self.handle_dns_destination_end = int(self.value_retry[12])
                                        self.rsync_last = int(self.value_retry[13])
                                        self.suspend = int(self.value_retry[14])
                                        self.remove = int(self.value_retry[15])
                                        self.client = int(self.value_retry[16])
                                        self.end_tasks = int(self.value_retry[17])
                                        self.thread_id_main = self.value_retry[18]
                                        self.register_type = int(self.value_retry[19])
                                        self.all_users = int(self.value_retry[20])
                                        if self.status == 2 and self.retry == 1:
                                            if self.found_error():
                                                if self.module_database.update_analyzing("retry", 0, self.thread_id):
                                                    if not self.not_send_message:
                                                        self.check_register_type()
                                                        self.message_manager()
                                                    self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                                                    if self.zen_return is not False and self.zen_return is not None and self.zen_return.status != "pending":
                                                        # update ticket
                                                        self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_handled, self.module_zen.tag_error)
                                                        self.zen_return.status = "pending"
                                                        # apply the change in ticket
                                                        self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                            else:
                                                self.module_database.update_analyzing("retry", 0, self.thread_id)
                                                self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Not match in found_error", self.thread_id), public=False, brand=self.brand)
                                                self._log.info("not match in found_error - {} - {}".format(self.ticket_id, self.thread_id))
                                                time.sleep(3)
                                                self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                                                if self.zen_return is not False and self.zen_return is not None:
                                                    # update ticket
                                                    self.zen_return.tags = self.module_zen.handle_tag(self.zen_return.tags, self.module_zen.tag_error, self.module_zen.tag_search_retry)
                                                    self.zen_return.status = "open"
                                                    # apply the change in ticket
                                                    self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                        else:
                                            self._log.info("status not error in ticket - {} - {}".format(self.ticket_id, self.thread_id))
                                    else:
                                        self._log.error("process_database retry failed in value retry check - '{}' - '{}'".format(__name__, self.ticket_id))

                                except Exception as er:
                                    # generate a error log
                                    self._log.error("for value retry - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id))
                                    continue

                    except Exception as er:
                        # generate a error log
                        self._log.error("process_database retry - '{}' - '{}' - '{}'".format(__name__, er, self.ticket_id))
                        continue

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(__name__, er))
            return False
