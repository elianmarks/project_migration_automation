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
from migration_automation_manager.module_ansible import ModuleAnsible
from migration_automation_manager.module_database import ModuleDatabase
from migration_automation_manager.module_publish import ModulePublish
import os
import datetime
import uuid
import json
from contextlib import closing


class ModuleHandleDNS:

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
            # set playbooks
            self.playbook_dns = self.module_configuration.playbook_dns
            # get values collected
            self.server = None
            self.values_ticket = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.main_domain = None
            self.ticket_id = None
            self.user = None
            self.destination_ip = None
            self.open_ips = None
            self.file_ips = None
            self.message = None
            self.destination_mail_ip = None
            self.file_account_summary = None
            self.open_account_summary = None
            self.account_summary = None
            self.open_ns_zones = None
            self.file_ns_zones = None
            self.type_key = None
            self.value_key = None
            self.thread_id = None
            self.type_task = None
            self.ns_zones = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
            self.file_hostname = None
            self.open_hostname = None
            self.values_database = None
            self.report_dir = self.module_configuration.report_dir
            self.summary_ansible = None
            self.hostname = None
            self.module_ansible = None
            self.vars_ansible = None
            self.report_casepath = None
            self.save_suspend_uuid = None
            self.queue_manager = ModulePublish(self._log, "manager", self.module_configuration.user_queue, self.module_configuration.password_queue,
                                               self.module_configuration.host_queue, self.module_configuration.port_queue, self.module_configuration.key("manager"))

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            self.general_error = True

    def initialize(self, values_ticket):
        try:
            # get values collected
            self.server = None
            self.values_ticket = None
            self.src_server = None
            self.dst_server = None
            self.src_type = None
            self.dst_type = None
            self.open_ns_zones = None
            self.file_ns_zones = None
            self.ns_zones = None
            self.destination_ip = None
            self.type_key = None
            self.main_domain = None
            self.ticket_id = None
            self.file_account_summary = None
            self.open_account_summary = None
            self.account_summary = None
            self.value_key = None
            self.user = None
            self.open_ips = None
            self.file_ips = None
            self.destination_mail_ip = None
            self.thread_id = None
            self.file_hostname = None
            self.hostname = None
            self.open_hostname = None
            self.type_task = None
            self.src_ip = None
            self.dst_ip = None
            self.connect_ip = None
            self.values_database = None
            self.module_ansible = None
            self.vars_ansible = None
            self.summary_ansible = False
            self.general_error = False
            # get values collected
            self.values_ticket = values_ticket
            self.ticket_id = self.values_ticket.get('id')
            self.thread_id = self.values_ticket.get('thread_id')
            self.type_task = self.values_ticket.get('type_task')
            self.save_suspend_uuid = str(uuid.uuid4())
            # get values in database
            if self.ticket_id is not None and self.ticket_id is not False and \
                    self.thread_id is not None and self.thread_id is not False and \
                    self.type_task is not None and self.type_task is not False:
                self.values_database = self.module_database.get_values(self.ticket_id, self.thread_id, "handle_dns")
                if self.values_database is not False and self.values_database is not None and len(self.values_database) == 9:
                    self.src_server = self.values_database[0]
                    self.dst_server = self.values_database[1]
                    self.src_type = self.values_database[2]
                    self.dst_type = self.values_database[3]
                    self.main_domain = self.values_database[4]
                    self.user = self.values_database[5]
                    self.src_ip = self.values_database[6]
                    self.dst_ip = self.values_database[7]
                    self.connect_ip = self.values_database[8]
                    self.report_casepath = os.path.join(self.report_dir, str(self.main_domain) + "_" + str(self.ticket_id) + "_" + str(self.thread_id))
                    # instance ansible module to all servers
                    self.module_ansible = ModuleAnsible(module_log=self._log, module_configuration=self.module_configuration)
                    if self.type_task == "source":
                        self.destination_ip = self.get_account_summary("ip", "destination_end")
                        if self.destination_ip is False or self.destination_ip is None:
                            self._log.error("Failed in destination_ip handle dns - {}".format(self.values_ticket))
                            self.general_error = True
                            return False
                        if self.dst_type == "vps" or self.dst_type == "dedi":
                            self.destination_mail_ip = self.get_destination_mail_ips()
                            if self.destination_mail_ip is False:
                                self.general_error = True
                                return False
                            # set ansible variables
                            self.vars_ansible = {
                                "destination_ip": self.destination_ip,
                                "user": self.user,
                                "type": self.type_task,
                                "dst_type": self.dst_type,
                                "destination_mail_ip": self.destination_mail_ip,
                                "ticketID": self.ticket_id,
                                "threadID": self.thread_id,
                                "domain": self.main_domain,
                                "saveSuspendUUID": self.save_suspend_uuid,
                            }
                        else:
                            # set ansible variables
                            self.vars_ansible = {
                                "destination_ip": self.destination_ip,
                                "user": self.user,
                                "type": self.type_task,
                                "dst_type": self.dst_type,
                                "ticketID": self.ticket_id,
                                "threadID": self.thread_id,
                                "domain": self.main_domain,
                                "saveSuspendUUID": self.save_suspend_uuid,
                            }
                        if self.connect_ip == 1 and self.src_ip is not None:
                            self.server = self.src_ip
                        else:
                            self.server = self.src_server
                        self.module_database.update_analyzing("handle_dns_date", datetime.datetime.now(), self.thread_id)
                        return True
                    elif self.type_task == "destination_end":
                        self.destination_ip = self.get_account_summary("ip", "destination_end")
                        if self.destination_ip is False or self.destination_ip is None:
                            self._log.error("Failed in destination_ip handle dns - {}".format(self.values_ticket))
                            self.general_error = True
                            return False
                        self.hostname = self.get_hostname()
                        if self.hostname is False or self.hostname is None:
                            self._log.error("Failed in hostname handle dns - {}".format(self.values_ticket))
                            self.general_error = True
                            return False
                        self.vars_ansible = {
                            "domain": self.main_domain,
                            "source_hostname": self.hostname,
                            "user": self.user,
                            "type": self.type_task,
                            "ticketID": self.ticket_id,
                            "threadID": self.thread_id,
                        }
                        if self.connect_ip == 1 and self.dst_ip is not None:
                            self.server = self.dst_ip
                        else:
                            self.server = self.dst_server
                        return True
                    else:
                        self.general_error = True
                        self._log.error("Invalid type handle dns - {}".format(self.values_ticket))
                        return False
                else:
                    self.general_error = True
                    self._log.error("Failed handle dns get values in database - {}".format(self.values_ticket))
                    return False
            else:
                self.general_error = True
                self._log.error("Failed handle dns get values in message - {}".format(self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("initialize handle dns - {} - {}".format(self.__class__.__name__, er))
            self.general_error = True
            return False

    def process(self):
        try:
            if self.general_error is False:
                # mark start ansible handle dns, 1 - start, 2 - failed, 3 - completed
                self.module_database.update_analyzing("handle_dns_" + self.type_task, 1, self.thread_id)
                # debug log
                self._log.debug(self.vars_ansible)
                # execute playbook and get summary result
                self.summary_ansible = self.module_ansible.execute(self.playbook_dns, self.vars_ansible, self.server)
                # check if execution completed with success
                if self.summary_ansible is False or self.summary_ansible is None:
                    # update cpanel type with failed
                    self.module_database.update_analyzing("handle_dns_" + self.type_task, 2, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # error log
                    self._log.error("Ansible handle dns failed - {} - {}".format(self.type_task, self.values_ticket))
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
                else:
                    # set completed with success in cpanel type
                    self.module_database.update_analyzing("handle_dns_" + self.type_task, 3, self.thread_id)
                    self.vars_ansible = None
                    self.summary_ansible = False
                    # debug log
                    self._log.debug("Ansible handle dns completed - {} - {}".format(self.type_task, self.values_ticket))
                    if self.message_manager():
                        self._log.info("Send manager {}".format(self.message))
                    else:
                        self._log.info("Failed send manager {}".format(self.message))
                return True
            else:
                # critical log
                self._log.critical("Error - generalError {} - values {}".format(self.general_error, self.values_ticket))
                return False

        except Exception as er:
            # generate a error log
            self._log.error("process handle dns - {} - {}".format(self.__class__.__name__, er))
            return False

    def message_manager(self):
        try:
            self.message = dict()
            self.message.update({'sender': 'handle_dns'})
            self.message.update({'id': self.ticket_id})
            self.message.update({'thread_id': self.thread_id})
            if self.get_ns_zones() and self.ns_zones is not False and self.ns_zones is not None and len(self.ns_zones) == 2:
                self.message.update({'ns_zones': self.ns_zones})
            else:
                self.message.update({'ns_zones': False})
            if self.destination_ip is not False and self.destination_ip is not None:
                self.message.update({'destination_ip': self.destination_ip})
            else:
                self.message.update({'destination_ip': False})
            self.queue_manager.publish(self.message)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("message handle dns - {} - {}".format(self.__class__.__name__, er))
            return False

    def get_account_summary(self, value_key, type_key):
        try:
            self.type_key = type_key
            self.value_key = value_key
            self.file_account_summary = os.path.join(self.report_casepath, self.type_key, "accountSummary.json")
            if os.path.exists(self.file_account_summary):
                with closing(open(self.file_account_summary)) as self.open_account_summary:
                    self.account_summary = json.load(self.open_account_summary)
                # check if result of the command is success and store in separate variables
                if int(self.account_summary['metadata']['result']) == 1 and self.account_summary['metadata']['reason'] == "OK":
                    return self.account_summary['data']['acct'][0][self.value_key]
                else:
                    return False
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("Get account summary in handle dns {} - {}".format(self.__class__.__name__, er))
            return False

    def get_hostname(self):
        try:
            if self.type_task == "source":
                self.file_hostname = os.path.join(self.report_casepath, "destination_end/hostname")
            elif self.type_task == "destination_end":
                self.file_hostname = os.path.join(self.report_casepath, "source/hostname")
            # check if file exists
            if os.path.exists(self.file_hostname):
                # open file and store in variable
                with closing(open(self.file_hostname)) as self.open_hostname:
                    return self.open_hostname.read()
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("Get hostname in handle dns {} - {}".format(self.__class__.__name__, er))
            return False

    def get_destination_mail_ips(self):
        try:
            self.file_ips = os.path.join(self.report_casepath, "destination_end/ips")
            # check if file exists
            if os.path.exists(self.file_ips):
                # open file and store in variable
                with closing(open(self.file_ips)) as self.open_ips:
                    return self.open_ips.read().splitlines()
            else:
                return False

        except Exception as er:
            # generate a error log
            self._log.error("Get ips in handle dns {} - {}".format(self.__class__.__name__, er))
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
            self._log.error("Get ns zones in manager {} - {}".format(self.__class__.__name__, er))
            return False
