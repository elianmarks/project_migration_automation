# -*- coding: utf-8 -*-
"""


- Contributors
Elliann Marks <elian.markes@gmail.com>





**- Version 1.0 - 18/09/2019**
**Functions - main**
**Libraries - ModuleMain and time**
**Dependencies - no**
**Parameters - no**

# Use PHP70 as default
AddHandler application/x-httpd-php70 .php
<IfModule mod_suphp.c>
    suPHP_ConfigPath /opt/php70/lib
</IfModule>

<IfModule mime_module>
  AddHandler application/x-httpd-ea-php56 .php .php5 .phtml
</IfModule>

# Use PHP70 as default
AddHandler application/x-httpd-php70 .php
<IfModule mod_suphp.c>
    suPHP_ConfigPath /opt/php70/lib
</IfModule>

# php -- BEGIN cPanel-generated handler, do not edit
# Set the “ea-php71” package as the default “PHP” programming language.
<IfModule mime_module>
  AddHandler application/x-httpd-ea-php71 .php .php7 .phtml
</IfModule>
# php -- END cPanel-generated handler, do not edit

"""

# libraries
from migration_automation_manager.module_database import ModuleDatabase
from migration_automation_manager.module_publish import ModulePublish
from migration_automation_manager.module_zen import ModuleZen
from migration_automation_manager.module_templates import ModuleTemplates
from sgqlc.endpoint.http import HTTPEndpoint
import os
import time


class ModuleManager:

    def __init__(self, module_log, module_configuration):
        """
        Responsible for execute the checking playbooks and store result in dict.
        :param module_log: log instance
        :type module_log: Object
        """
        try:
            self._log = module_log
            self.module_configuration = module_configuration
            self.url_graphql = "https://api.example.com"
            self.general_error = False
            # create the instances
            self.module_database = ModuleDatabase(self._log, self.module_configuration)
            self.module_zen = ModuleZen(self._log, self.module_configuration)
            self.module_templates = ModuleTemplates(self._log)
            # get values collected
            self.ticket_id = None
            self.thread_id = None
            self.type_task = None
            self.sender = None
            self.values_database = None
            self.user = None
            self.check_source = None
            self.check_destination = None
            self.cpanel_pkgacct = None
            self.cpanel_restore = None
            self.rsync = None
            self.suspend = None
            self.remove = None
            self.suspend_date = None
            self.ns_zones = None
            self.remove_date = None
            self.handle_dns_date = None
            self.compare = None
            self.mysql_version_src = None
            self.mysql_version_dst = None
            self.checking_mysql = None
            self.handle_dns_source = None
            self.handle_dns_destination_end = None
            self.home = None
            self.handled = None
            self.status = None
            self.src_server = None
            self.dst_server = None
            self.this_owner = None
            self.src_type = None
            self.dst_type = None
            self.available_user = None
            self.main_domain = None
            self.report_casepath = None
            self.zen_return = None
            self.report_dir = self.module_configuration.report_dir
            self.message = None
            self.check_destination_end = None
            self.values_ticket = None
            self.rsync_last = None
            self._check_error = None
            self._value_error = None
            self.destination_ip = None
            self.client = None
            self.all_users = None
            self.request_type = None
            self.brand_graphql = None
            self.variables_graphql = None
            self.query_graphql = None
            self.endpoint_graphql = None
            self.data_graphql = None
            self.result_graphql = None
            self.result_code_graphql = None
            self.result_data_graphql = None
            self.end_tasks = None
            self.brand = None
            self.file_open_view_transfer_command = None
            self.file_view_transfer_command = None
            self.content_view_transfer_command = None
            self.queue_check = ModulePublish(self._log, "check", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                             self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("check"))
            self.queue_cpanel = ModulePublish(self._log, "cpanel", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                              self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("cpanel"))
            self.queue_rsync = ModulePublish(self._log, "rsync", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                             self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("rsync"))
            self.queue_rsync_last = ModulePublish(self._log, "rsync_last", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                                  self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("rsync_last"))
            self.queue_check_end = ModulePublish(self._log, "check_end", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                                 self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("check_end"))
            self.queue_compare = ModulePublish(self._log, "compare", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                               self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("compare"))
            self.queue_handle_dns = ModulePublish(self._log, "handle_dns", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                                  self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("handle_dns"))
            self.queue_handle_account = ModulePublish(self._log, "handle_account", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                                      self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("handle_account"))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            self.general_error = True

    def initialize(self, values_ticket):
        try:
            # get values collected
            self.values_ticket = None
            self.ticket_id = None
            self.thread_id = None
            self.type_task = None
            self.sender = None
            self.values_database = None
            self.user = None
            self.ns_zones = None
            self.src_server = None
            self._check_error = None
            self._value_error = None
            self.dst_server = None
            self.client = None
            self.src_type = None
            self.dst_type = None
            self.this_owner = None
            self.check_destination_end = None
            self.main_domain = None
            self.check_source = None
            self.check_destination = None
            self.cpanel_pkgacct = None
            self.cpanel_restore = None
            self.mysql_version_src = None
            self.mysql_version_dst = None
            self.brand = None
            self.checking_mysql = None
            self.rsync_last = None
            self.rsync = None
            self.zen_return = None
            self.compare = None
            self.handle_dns_source = None
            self.handle_dns_destination_end = None
            self.home = None
            self.handled = None
            self.available_user = None
            self.status = None
            self.suspend = None
            self.remove = None
            self.suspend_date = None
            self.remove_date = None
            self.handle_dns_date = None
            self.destination_ip = None
            self.request_type = None
            self.brand_graphql = None
            self.variables_graphql = None
            self.query_graphql = None
            self.endpoint_graphql = None
            self.data_graphql = None
            self.result_graphql = None
            self.result_code_graphql = None
            self.result_data_graphql = None
            self.end_tasks = None
            self.all_users = None
            self.file_open_view_transfer_command = None
            self.file_view_transfer_command = None
            self.content_view_transfer_command = None
            self.general_error = False
            # get values collected
            self.values_ticket = values_ticket
            self.ticket_id = self.values_ticket.get('id')
            self.thread_id = self.values_ticket.get('thread_id')
            self.sender = self.values_ticket.get('sender')
            # get values in database
            if self.ticket_id is not None and self.ticket_id is not False and \
                    self.thread_id is not None and self.thread_id is not False and \
                    self.sender is not None and self.sender is not False:
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "manager")
                self._log.debug("Manager values in database - {}".format(self.values_database))
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 30:
                    self.src_server = self.values_database[0]
                    self.dst_server = self.values_database[1]
                    self.src_type = self.values_database[2]
                    self.dst_type = self.values_database[3]
                    self.main_domain = self.values_database[4]
                    self.user = self.values_database[5]
                    self.check_source = int(self.values_database[6])
                    self.check_destination = int(self.values_database[7])
                    self.cpanel_pkgacct = int(self.values_database[8])
                    self.cpanel_restore = int(self.values_database[9])
                    self.client = int(self.values_database[10])
                    self.brand = self.values_database[11]
                    self.rsync = int(self.values_database[12])
                    self.all_users = int(self.values_database[13])
                    self.home = self.values_database[14]
                    self.handled = int(self.values_database[15])
                    self.status = int(self.values_database[16])
                    self.check_destination_end = int(self.values_database[17])
                    self.compare = int(self.values_database[18])
                    self.handle_dns_source = int(self.values_database[19])
                    self.handle_dns_destination_end = int(self.values_database[20])
                    self.rsync_last = int(self.values_database[21])
                    self.suspend = int(self.values_database[22])
                    self.remove = int(self.values_database[23])
                    self.suspend_date = self.values_database[24]
                    self.remove_date = self.values_database[25]
                    self.handle_dns_date = self.values_database[26]
                    self.request_type = self.values_database[27]
                    self.end_tasks = self.values_database[28]
                    self.this_owner = self.values_database[29]
                    self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                    return True
                else:
                    self.general_error = True
                    self._log.error("Failed manager get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed manager get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize manager - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                # check error in execution
                self._check_error, self._value_error = self.check_error()
                if self._check_error:
                    self.module_database.update_analyzing("status", 2, self.thread_id)
                    self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error(self._value_error, self.thread_id), public=False, brand=self.brand)
                    self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                    if self.zen_return is not False:
                        self.zen_return.tags = self.module_zen.tag_error
                        self.zen_return.assignee = None
                        self.zen_return.status = "open"
                        self.zen_return.priority = "high"
                        # apply the change in ticket
                        self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                        self._log.info("Failed in ticket - {}".format(self.values_ticket))
                    else:
                        self._log.error("Error in get ticket - {}".format(self.values_ticket))
                else:
                    # check message and sender to execute action
                    if self.sender == "check" and self.check_source == 3 and self.check_destination == 3 and self.cpanel_pkgacct == 0 and self.cpanel_restore == 0 and self.rsync == 0:
                        self._log.debug("Enter in check sender")
                        self.message_cpanel("pkgacct")
                    elif self.sender == "check" and self.check_source == 3 and self.check_destination == 0 and self.cpanel_pkgacct == 0 and self.cpanel_restore == 0 and self.rsync == 0:
                        self._log.debug("Enter in check sender")
                        self.message_check("destination")
                    elif (self.sender == "zencheck" or self.sender == "bdcheck") and self.check_source == 0 and self.check_destination == 0 and self.cpanel_pkgacct == 0 and self.cpanel_restore == 0 and self.rsync == 0:
                        self._log.debug("Enter in zencheck or bdcheck sender")
                        self.message_check("source")
                    elif self.sender == "cpanel" and self.cpanel_restore == 0 and self.cpanel_pkgacct == 3 and self.rsync == 0:
                        self._log.debug("Enter in cpanel sender")
                        self.available_user = self.values_ticket.get('available_user')
                        if self.available_user is True:
                            self.message_cpanel("restore")
                        else:
                            self.module_database.update_analyzing("status", 2, self.thread_id)
                            self.module_database.update_analyzing("cpanel_restore", 2, self.thread_id)
                            self._log.info("User not available in destination server - {}".format(self.values_ticket))
                            self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("User - {} - not available in destination server".format(self.user), self.thread_id), public=False, brand=self.brand)
                            self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                            if self.zen_return is not False:
                                self.zen_return.tags = self.module_zen.tag_error
                                self.zen_return.assignee = None
                                self.zen_return.status = "open"
                                self.zen_return.priority = "high"
                                self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                    elif self.sender == "cpanel" and self.cpanel_restore == 3 and self.rsync == 0 and self.cpanel_pkgacct == 3:
                        self._log.debug("Enter in cpanel sender with restore completed")
                        self.view_transfer_command()
                        self.message_rsync()
                    elif self.sender == "rsync" and self.cpanel_restore == 3 and self.rsync == 3 and self.cpanel_pkgacct == 3 and self.check_destination_end == 0 and \
                            self.handle_dns_destination_end == 0 and self.handle_dns_source == 0:
                        self._log.debug("Enter in rsync sender - {}".format(self.values_ticket))
                        self.message_check_end()
                    elif self.sender == "rsync" and self.cpanel_restore == 3 and self.cpanel_pkgacct == 3 and \
                            self.rsync == 3 and self.check_source == 3 and \
                            self.check_destination == 3 and self.check_destination_end == 3 and self.compare == 0 and \
                            self.handle_dns_destination_end == 3 and self.handle_dns_source == 3 and self.rsync_last == 1 and self.status == 3:
                        self._log.debug("Enter in rsync sender for compare- {}".format(self.values_ticket))
                        self.message_compare()
                        self.module_database.update_analyzing("rsync_last", 3, self.thread_id)
                    elif self.sender == "check_end" and self.cpanel_restore == 3 and self.rsync == 3 and self.cpanel_pkgacct == 3 and \
                            self.check_destination_end == 3 and self.status == 1 and self.handle_dns_source == 0 and self.rsync_last == 0:
                        self._log.debug("Enter in check_end sender - {}".format(self.values_ticket))
                        self.message_handle_dns("source")
                    elif self.sender == "handle_dns" and self.cpanel_restore == 3 and self.rsync == 3 and self.cpanel_pkgacct == 3 and \
                            self.check_destination_end == 3 and self.handle_dns_destination_end == 0 and self.handle_dns_source == 3 and \
                            self.rsync_last == 0 and self.status == 1:
                        self._log.debug("Enter in handle_dns for destination_end - {}".format(self.values_ticket))
                        self.message_handle_dns("destination_end")
                        self.get_mysql_version()
                        if self.checking_mysql is True and self.mysql_version_src is not None and self.mysql_version_dst is not None \
                                and self.mysql_version_src is not False and self.mysql_version_dst is not False:
                            self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_mysql_version(self.mysql_version_src, self.mysql_version_dst), public=False, brand=self.brand)
                    elif self.sender == "compare" and self.cpanel_restore == 3 and self.cpanel_pkgacct == 3 and \
                            self.rsync == 3 and self.check_source == 3 and \
                            self.check_destination == 3 and self.check_destination_end == 3 and \
                            self.handle_dns_destination_end == 3 and self.handle_dns_source == 3 and self.rsync_last == 3 and self.status == 3:
                        self.message_handle_account("suspend")
                    elif self.sender == "handle_account" and self.cpanel_restore == 3 and self.cpanel_pkgacct == 3 and \
                            self.rsync == 3 and self.check_source == 3 and \
                            self.check_destination == 3 and self.check_destination_end == 3 and \
                            self.handle_dns_destination_end == 3 and self.handle_dns_source == 3 and self.rsync_last == 3 and self.status == 3:
                        self._log.debug("Enter in handle_account for check_end - {}".format(self.values_ticket))
                        self.message_check_end()
                    elif self.sender == "handle_dns" and self.cpanel_restore == 3 and self.cpanel_pkgacct == 3 and \
                            self.rsync == 3 and self.check_source == 3 and \
                            self.check_destination == 3 and self.check_destination_end == 3 and \
                            self.handle_dns_destination_end == 3 and self.handle_dns_source == 3 and self.rsync_last == 0:
                        self._log.debug("Enter in handler_dns sender - {}".format(self.values_ticket))
                        self.module_database.update_analyzing("rsync_last", 1, self.thread_id)
                        if self.this_owner is not None and self.this_owner == 1:
                            self.module_database.update_analyzing("owner_status", 3, self.thread_id)
                        self.message_rsync_last()
                        self.module_database.update_analyzing("status", 3, self.thread_id)
                        if self.end_tasks == 0 and self.this_owner == 0 and self.client == 0 and self.all_users == 0 and self.dst_type != "vps" and self.dst_type != "dedi":
                            self.module_database.update_analyzing("end_tasks", 1, self.thread_id)
                            self.change_server(self.brand)
                            # self.zen_return = self.module_zen.macro(self.ticket_id, self.module_zen.macro_finish_shared_id)
                            # self.zen_return.ticket.comment.html_body = self.zen_return.ticket.comment.html_body.replace("$DNS1", self.ns_zones[0].replace("ns=", "")).replace("$DNS2", self.ns_zones[1].replace("ns=", ""))
                            # self.zen_return.ticket.comment.html_body = self.zen_return.ticket.comment.body.replace("$DNS1", self.ns_zones[0].replace("ns=", "")).replace("$DNS2", self.ns_zones[1].replace("ns=", ""))
                            # self.zen_return.ticket.tags = self.module_zen.tag_completed
                            # self.zen_return.ticket.assignee = None
                            # self.zen_return.ticket.status = "pending"
                            # self.module_zen.update_ticket(self.zen_return, type_macro=True)
                            self.ns_zones = self.values_ticket.get('ns_zones')
                            self.destination_ip = self.values_ticket.get('destination_ip')
                            if self.ns_zones is not None and self.ns_zones is not False and self.destination_ip is not None and self.destination_ip is not False:
                                if (self.request_type == 1 and self.module_zen.comment_ticket(self.ticket_id, self.module_templates.turbo_completed(self.ns_zones, self.destination_ip, brand=self.brand), brand=self.brand)) or \
                                        (self.request_type == 2 and self.module_zen.comment_ticket(self.ticket_id, self.module_templates.monitoring_completed(self.ns_zones, self.destination_ip, brand=self.brand), brand=self.brand)):
                                    self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
                                    time.sleep(3)
                                    if self.zen_return is not False:
                                        self.zen_return.tags = self.module_zen.tag_completed
                                        self.zen_return.assignee = None
                                        self.zen_return.status = "pending"
                                        self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                                        self._log.info("Completed ticket - {}".format(self.values_ticket))
                                else:
                                    self._log.error("Comment completed ticket failed - {}".format(self.values_ticket))
                            else:
                                self.error_ns_zones()
                    else:
                        self._log.debug("Message not match - {}".format(self.values_ticket))
            else:
                # critical log
                self._log.critical("Error manager - generalError {} - values {}".format(self.general_error, self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("process manager - {} - {}".format(self.__class__.__name__, er))
            return False

    def view_transfer_command(self):
        try:
            self.file_view_transfer_command = os.path.join(self.report_casepath, "view_transfer_command")
            if os.path.exists(self.file_view_transfer_command):
                self.file_open_view_transfer_command = open(self.file_view_transfer_command, "r")
                self.content_view_transfer_command = self.file_open_view_transfer_command.read()
                if self.content_view_transfer_command is not None and self.content_view_transfer_command is not False and \
                        len(self.content_view_transfer_command) > 12:
                    self.module_zen.comment_ticket(self.ticket_id, "User: {}\n\nThread ID: {}\n\nRestore check: {}".format(self.user, self.thread_id, self.content_view_transfer_command),
                                                   public=False, brand=self.brand)

        except Exception as er:
            # generate a error log
            self._log.error("view_transfer_command - {} - {}".format(self.__class__.__name__, er))
            return False

    def get_mysql_version(self):
        try:
            self.checking_mysql = self.values_ticket.get('checking_mysql')
            self.mysql_version_src = self.values_ticket.get('mysql_version_src')
            self.mysql_version_dst = self.values_ticket.get('mysql_version_dst')

        except Exception as er:
            # generate a error log
            self._log.error("error get mysql version - {} - {}".format(self.__class__.__name__, er))
            return False

    def error_ns_zones(self):
        try:
            self._log.error("Error in get and handle ns zones / destination ip - {}".format(self.values_ticket))
            self.module_database.update_analyzing("status", 2, self.thread_id)
            self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Error in get and handle ns zones / destination ip.", self.thread_id), public=False, brand=self.brand)
            self.zen_return = self.module_zen.search_id(self.ticket_id, brand=self.brand)
            if self.zen_return is not False:
                self.zen_return.tags = self.module_zen.tag_error
                self.zen_return.assignee = None
                self.zen_return.status = "open"
                self.zen_return.priority = "high"
                # apply the change in ticket
                self.module_zen.update_ticket(self.zen_return, brand=self.brand)
                self._log.info("Error in ticket - {}".format(self.values_ticket))

        except Exception as er:
            # generate a error log
            self._log.error("error ns zones - {} - {}".format(self.__class__.__name__, er))
            return False

    def check_error(self):
        try:
            if self.cpanel_restore == 2:
                self.view_transfer_command()
                return True, "cpanel_restore"
            elif self.cpanel_pkgacct == 2:
                return True, "cpanel_pkgacct"
            elif self.rsync == 2:
                return True, "rsync"
            elif self.check_source == 2:
                if os.path.exists(os.path.join(self.report_casepath, "account_suspended.flag")):
                    self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error("Error because account is suspended, require unsuspend.", self.thread_id),
                                                   public=False, brand=self.brand)
                return True, "check_source"
            elif self.check_destination == 2:
                return True, "check_destination"
            elif self.check_destination_end == 2:
                return True, "check_destination_end"
            elif self.handle_dns_destination_end == 2:
                return True, "handle_dns_destination_end"
            elif self.handle_dns_source == 2:
                return True, "handle_dns_source"
            elif self.suspend == 2:
                return True, "suspend"
            elif self.remove == 2:
                return True, "remove"
            elif self.compare == 2:
                return True, "compare"
            elif self.status == 2:
                return True, "status"
            else:
                return False, None

        except Exception as er:
            # generate a error log
            self._log.error("check_error - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_check(self, type_task):
        try:
            self.type_task = type_task
            self.message = dict()
            self.message.update({'type_task': self.type_task})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_check.publish(self.message)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message check - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_cpanel(self, type_task):
        try:
            self.type_task = type_task
            self.message = dict()
            self.message.update({'type_task': self.type_task})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_cpanel.publish(self.message)
            self._log.debug("Message cpanel {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message cpanel - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_rsync(self):
        try:
            self.message = dict()
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_rsync.publish(self.message)
            self._log.debug("Message rsync {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message rsync - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_rsync_last(self):
        try:
            self.message = dict()
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_rsync_last.publish(self.message)
            self._log.debug("Message rsync last {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message rsync last - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_check_end(self):
        try:
            self.message = dict()
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_check_end.publish(self.message)
            self._log.debug("Message check end {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message check end - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_compare(self):
        try:
            self.message = dict()
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_compare.publish(self.message)
            self._log.debug("Message compare {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message compare - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_handle_dns(self, type_task):
        try:
            self.type_task = type_task
            self.message = dict()
            self.message.update({'type_task': self.type_task})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_handle_dns.publish(self.message)
            self._log.debug("Message handle_dns {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message handle_dns - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_handle_account(self, type_task):
        try:
            self.type_task = type_task
            self.message = dict()
            self.message.update({'type_task': self.type_task})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            self.queue_handle_account.publish(self.message)
            self._log.debug("Message handle_account {}".format(self.message))
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message handle account - {} - {}".format(self.__class__.__name__, er))
            return False

    def change_server(self, brand="br"):
        try:
            self.brand_graphql = brand
            self.module_database.update_analyzing("change_server", 1, self.thread_id)
            self.query_graphql = '''query (
                                $originServer: String!,
                                $destinationServer: String!,
                                $username: String!,
                                $brand: String!,
                                $token: String
                                )
                            {
                            changeServer (
                                originServer: $originServer
                                destinationServer: $destinationServer
                                username: $username
                                brand: $brand
                                token: $token
                            ) { 
                                result, httpStatusCode, message 
                                } 
                            }'''
            self.variables_graphql = {
                'originServer': self.src_server,
                'destinationServer': self.dst_server,
                'username': self.user,
                'brand': self.brand_graphql,
                'token': self.module_configuration.token_whmcs
            }
            self.endpoint_graphql = HTTPEndpoint(self.url_graphql)
            self.data_graphql = self.endpoint_graphql(self.query_graphql, self.variables_graphql)
            self.result_graphql = self.data_graphql.get('data').get('changeServer').get('result')
            self.result_code_graphql = self.data_graphql.get('data').get('changeServer').get('httpStatusCode')
            self.result_data_graphql = self.data_graphql.get('data').get('changeServer').get('message')
            if self.result_graphql and self.result_code_graphql == 200:
                self.module_database.update_analyzing("change_server", 3, self.thread_id)
                self._log.info("WHMCS - Change server completed - {}".format(self.thread_id))
                self.module_zen.comment_ticket(self.ticket_id, "WHMCS - Change server completed", public=False, brand=self.brand)
                return True
            else:
                self.module_database.update_analyzing("change_server", 2, self.thread_id)
                self._log.info("WHMCS - Change server failed - {}".format(self.thread_id))
                if self.result_data_graphql is not None and self.result_data_graphql is not False:
                    self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error(
                        "WHMCS - Change server failed - {}".format(self.result_data_graphql), self.thread_id), public=False, brand=self.brand)
                    return False
                else:
                    self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error(
                        "WHMCS - Change server failed", self.thread_id), public=False, brand=self.brand)
                    return False

        except Exception as er:
            self.module_database.update_analyzing("change_server", 2, self.thread_id)
            # generate a error log
            self._log.error("change server - {} - {}".format(self.__class__.__name__, er))
            self.module_zen.comment_ticket(self.ticket_id, self.module_zen.comment_error(
                        "WHMCS - Change server failed", self.thread_id), public=False, brand=self.brand)
            return False
