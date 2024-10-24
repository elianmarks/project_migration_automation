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
from migration_automation_manager.module_connectdb import ModuleConnectDB
from contextlib import closing


class ModuleDatabase:

    def __init__(self, module_log, module_configuration):
        """
        Create instance of the ModuleConnectDB class.
        :param module_log: Instance of the log class
        :type module_log: object
        """
        self.module_configuration = module_configuration
        self._log = module_log
        # create instance with connection for database
        self._module_connectDB = ModuleConnectDB(module_log, self.module_configuration)
        # create privates variables
        self._cursor = None
        self._sql = None
        self._conn = None
        self._cursor = None
        self.result_DB = None
        self.value = None
        self.column = None
        self.thread_id = None
        self.ticket_id = None
        self.src_server = None
        self.dst_server = None
        self.main_domain = None
        self.destination = None
        self.owner = None
        self.thread_id_main = None
        self.brand = None
        self.source_database = None
        self.type_values = None

    def check_thread_id(self, thread_id):
        try:
            self.thread_id = thread_id
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select ticket_id from analyzing where thread_id = '{}' order by id desc limit 1".format(self.thread_id)
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchone()
                        # check if a line has been found
                        if self._cursor.rowcount == 1:
                            return True
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def check_duplicated(self, src_server, dst_server, main_domain, source_database=None):
        try:
            self.src_server = src_server
            self.dst_server = dst_server
            self.main_domain = main_domain
            self.source_database = source_database
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select ticket_id from analyzing where src_server = '{}' and " \
                                    "dst_server = '{}' and main_domain = '{}' " \
                                    "order by id desc limit 1".format(self.src_server, self.dst_server, self.main_domain)
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchone()
                        if self.source_database is None:
                            # check if a line has been found
                            if self._cursor.rowcount == 0:
                                return True
                            else:
                                return False
                        else:
                            # check if a line has been found
                            if self._cursor.rowcount == 1:
                                return True
                            else:
                                return False

                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_register_migrations(self):
        try:
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select src_server, dst_server, main_domain, ticket_id, force_ns, specific_migration, " \
                                    "this_owner, all_users, list_migration, src_ip, dst_ip, connect_ip, brand from analyzing " \
                                    "where register_type = 2 and status = 0 and check_source = 0 and handled = 1"
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_owners_completed(self):
        try:
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select src_server, dst_server, main_domain, ticket_id, force_ns, specific_migration, thread_id, list_migration, user, dst_ip, src_ip, connect_ip, brand " \
                                    "from analyzing where register_type = 2 and status = 3 and this_owner = 1 and owner_status = 3 and check_clients = 0"
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_db_retry(self):
        try:
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select ticket_id from analyzing where retry = 1 and status = 2"
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_results_shared(self):
        try:
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select thread_id, ticket_id, user, main_domain, brand " \
                                    "from analyzing where register_type = 2 and status = 3 and " \
                                    "src_type = 'shared' and (dst_type = 'reseller' or dst_type = 'vps' or dst_type = 'dedi') and end_ticket = 0"
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_results_reseller(self):
        try:
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select thread_id, ticket_id, user, main_domain, specific_migration, count_specific_migration, all_users, check_allusers, this_owner, check_clients, brand " \
                                    "from analyzing where register_type = 2 and status = 3 and " \
                                    "this_owner = 1 and owner_status = 3 and check_clients = 3 and end_ticket = 0"
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_results_allusers(self):
        try:
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select thread_id, ticket_id, user, main_domain, specific_migration, count_specific_migration, all_users, check_allusers, " \
                                    "this_owner, check_clients, brand from analyzing where register_type = 2 and all_users = 3 and  " \
                                    "check_allusers = 3 and status = 3 and end_ticket = 0 and (src_type = 'vps' or src_type = 'dedi')"
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_check_clients(self, thread_id_main):
        try:
            self.thread_id_main = thread_id_main
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select thread_id, ticket_id, user, main_domain, status from analyzing where " \
                                    "thread_id_main = '{}' and (client = 1 or thread_id_main = thread_id) and end_tasks = 0".format(self.thread_id_main)
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_check_completed(self, thread_id_main):
        try:
            self.thread_id_main = thread_id_main
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select thread_id, ticket_id, user, main_domain, status from analyzing where " \
                                    "thread_id_main = '{}' and end_tasks = 1 and (client = 3 or client = 2)".format(self.thread_id_main)
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB, self._cursor.rowcount
                        else:
                            return False, False
                else:
                    return False, False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False, False

    def get_allusers_completed(self):
        try:
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        self._sql = "select src_server, dst_server, main_domain, ticket_id, force_ns, specific_migration, thread_id, list_migration, dst_ip, src_ip, connect_ip, brand " \
                                    "from analyzing where register_type = 2 and all_users = 3 and check_allusers = 0 and check_source = 3 and (src_type = 'vps' or src_type = 'dedi')"
                        self._cursor.execute(self._sql)
                        self.result_DB = self._cursor.fetchall()
                        # check if a line has been found
                        if self._cursor.rowcount >= 1:
                            return self.result_DB
                        else:
                            return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def get_values(self, ticket_id, thread_id=None, type_values=None):
        try:
            self.type_values = type_values
            self.thread_id = thread_id
            self.ticket_id = ticket_id
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        if self.type_values == "handle_account":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, user," \
                                        "check_source, check_destination, cpanel_pkgacct, cpanel_restore," \
                                        "request_type, handle_dns_date, rsync, all_users, home, handled, status, check_destination_end," \
                                        "compare, handle_dns_source, handle_dns_destination_end, rsync_last, suspend, remove, " \
                                        "suspend_date, remove_date, src_ip, dst_ip, connect_ip from analyzing " \
                                        "where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id, self.ticket_id)
                        elif self.type_values == "manager":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, user," \
                                        "check_source, check_destination, cpanel_pkgacct, cpanel_restore," \
                                        "client, brand, rsync, all_users, home, handled, status, check_destination_end," \
                                        "compare, handle_dns_source, handle_dns_destination_end, rsync_last, suspend, remove, " \
                                        "suspend_date, remove_date, handle_dns_date, request_type, end_tasks, this_owner from analyzing " \
                                        "where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                             self.ticket_id)
                        elif self.type_values == "check":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, src_ip, dst_ip, connect_ip from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "handle_report":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "check_destination":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, user, src_ip, dst_ip, connect_ip from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "handle_php":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, user, src_ip, dst_ip, connect_ip from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "compare":
                            self._sql = "select main_domain, request_type from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "cpanel":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, user, src_ip, dst_ip, connect_ip from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "handle_dns":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, user, src_ip, dst_ip, connect_ip from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "rsync":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, home, home_destination, user, src_ip, dst_ip, connect_ip from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "retry":
                            self._sql = "select check_source, check_destination, cpanel_pkgacct, cpanel_restore," \
                                        "brand, thread_id, rsync, retry, status, check_destination_end," \
                                        "compare, handle_dns_source, handle_dns_destination_end, rsync_last, suspend, remove, client, end_tasks, thread_id_main, register_type, all_users " \
                                        "from analyzing where ticket_id = '{}'".format(self.ticket_id)
                        elif self.type_values == "mysql":
                            self._sql = "select src_server, dst_server, src_type, dst_type, main_domain, src_ip, dst_ip, connect_ip from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        elif self.type_values == "retry_main":
                            self._sql = "select end_ticket from " \
                                        "analyzing where thread_id = '{}' and ticket_id = '{}'".format(self.thread_id,
                                                                                                       self.ticket_id)
                        else:
                            return False
                        self._cursor.execute(self._sql)
                        if self.type_values == "retry":
                            self.result_DB = self._cursor.fetchall()
                            # check if lines has been found
                            if self._cursor.rowcount >= 1:
                                return self.result_DB
                            else:
                                return False
                        else:
                            self.result_DB = self._cursor.fetchone()
                            # check if a line has been found
                            if self._cursor.rowcount == 1:
                                return self.result_DB
                            else:
                                return False
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def update_analyzing(self, column, value, thread_id=None, ticket_id=None, main_domain=None):
        try:
            if value is True:
                self.value = 1
            elif value is False or value is None:
                self.value = 0
            else:
                self.value = value
            self.thread_id = thread_id
            self.ticket_id = ticket_id
            self.main_domain = main_domain
            self.column = column
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        if self.thread_id is not None:
                            self._sql = "update analyzing set {} = '{}' where thread_id = '{}'".format(self.column, self.value, self.thread_id)
                        elif self.ticket_id is not None and self.main_domain is None:
                            self._sql = "update analyzing set {} = '{}' where ticket_id = '{}'".format(self.column, self.value, self.ticket_id)
                        elif self.ticket_id is not None and self.main_domain is not None:
                            self._sql = "update analyzing set {} = '{}' where ticket_id = '{}' and main_domain = '{}'".format(self.column, self.value, self.ticket_id, self.main_domain)
                        else:
                            return False
                        self._cursor.execute(self._sql)
                        self._conn.commit()
                        return True
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False

    def insert_analyzing(self, ticket_id, thread_id, brand="br"):
        try:
            self.brand = brand
            self.ticket_id = ticket_id
            self.thread_id = thread_id
            # initialize connection with database
            with closing(self._module_connectDB.connection) as self._conn:
                # verify success in connection
                if self._conn is not False:
                    with closing(self._conn.cursor()) as self._cursor:
                        # check if duplicated is set
                        # sql for insert of the data
                        self._sql = "insert into analyzing(ticket_id, thread_id, brand) values('{}', '{}', '{}')".format(self.ticket_id, self.thread_id, self.brand)
                        self._cursor.execute(self._sql)
                        self._conn.commit()
                        return True
                else:
                    return False

        except Exception as er:
            # generate a error log
            self._log.error("{} - {}".format(self.__class__.__name__, er))
            return False
