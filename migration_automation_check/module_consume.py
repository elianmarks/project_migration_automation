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
import pika
import json
import time
from migration_automation_manager.module_log import ModuleLog
from migration_automation_manager.module_configuration import ModuleConfiguration
from migration_automation_check.module_check import ModuleCheck


class ModuleConsume:

    def __init__(self, queue, development=None):
        self.development = development
        self.module_configuration = None
        self.module_log = None
        # call configInit and check return
        if not self.config_init():
            # exit with code 3 if false return
            exit(3)
        self._log = self.module_log.log
        self._queue = queue
        # get host, key, user and password of the broker
        self._host = self.module_configuration.host_queue
        self._user = self.module_configuration.user_queue
        self._password = self.module_configuration.password_queue
        self._port = self.module_configuration.port_queue
        self._key = self.module_configuration.key(self._queue)
        # create credentials object
        self._credentials = pika.PlainCredentials(self._user, self._password)
        # define none variables
        self._connection = None
        self._channel = None
        self._values = None
        self._retry = 0
        # create ModuleAnalyze instance
        self.module_check = ModuleCheck(self.module_log.log, self.module_configuration)

    def config_init(self):
        """
        Responsible for create ModuleConfiguration and ModuleLog instances
        :return: True in success and False in error
        :rtype: bool
        """
        try:
            # instance module configuration
            self.module_configuration = ModuleConfiguration(self.development)
            if not self.module_configuration.initialize():
                # only print the error, since moduleLog there isn't instance
                print("Error in moduleConfiguration")
                return False
            else:
                # instance the ModuleLog class to Check path log (5)
                self.module_log = ModuleLog(self.module_configuration, 5)
                if not self.module_log.initialize():
                    # only print the error, since moduleLog there isn't instance
                    print("Error in initialize moduleLog")
                    return False
                else:
                    return True

        except Exception as er:
            # only print the error, since moduleLog there isn't instance
            print("{} - {}".format(__name__, er))
            return False

    @property
    def connection(self):
        """
        Responsible for create AMQP connection, define what queue will consume and parameters of the queue.
        **connection** - BlockingConnection instance
        **channel** - channel of the connection
        :return: True in success and False in error
        :rtype: bool
        """
        try:
            # create BlockingConnection instance using pika library
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host, port=self._port, credentials=self._credentials, heartbeat=900))
            # define channel variable and parameters of the queue
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._queue, durable=True)
            self._channel.basic_qos(prefetch_count=1)
            self._channel.basic_consume(queue=self._queue, on_message_callback=self.callback)
            return True

        except Exception as er:
            # generate a error log
            self._log.error("Pull - {} - {}".format(self.__class__.__name__, er))
            return False

    def consume(self):
        """
        Run start_consuming in channel instance, this is a loop that in case of error, wait 60 seconds and return loop
        """
        while True:
            try:
                self._connection = self.connection
                # check success in connection
                if self._connection is not None and self._connection is not False:
                    # run start consuming
                    self._channel.start_consuming()

            except Exception as er:
                # generate a error log
                self._log.error("{} - {}".format(self.__class__.__name__, er))
                # wait 60 seconds
                time.sleep(60)
                continue

    def callback(self, ch, method, properties, body):
        """
        Responsible for performing ModulePull functions.
        **values** - dict with message value
        """
        try:
            # send ack before treating message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            # load json body in variable values
            self._values = json.loads(body)
            # debug log
            self._log.debug(self._values)
            # check key value in header of the message, this must be equal to the value set in the configuration
            if properties.headers.get("x-key") is not None and \
                    str(properties.headers.get("x-key")) == str(self.module_configuration.key(self._queue)):
                # initialize variables in analyze
                if self.module_check.initialize(self._values):
                    # run process in check
                    self.module_check.process()
                    # info log completed process
                    self._log.info("Check process completed - {}".format(self._values))
            else:
                # error log with invalid key
                self._log.error("Invalid key check - {}".format(self._values))

        except Exception as er:
            # generate a error log
            self._log.error("Check - {} - {}".format(self.__class__.__name__, er))
            return False
