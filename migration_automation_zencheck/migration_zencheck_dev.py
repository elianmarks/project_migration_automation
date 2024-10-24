#!/usr/bin/env python3.7
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
from migration_automation_zencheck.module_zencheck import ModuleZencheck
import time


def main():
    try:
        # create ModuleMain instance
        module_zencheck = ModuleZencheck(development=True)
        # enter in loop
        while True:
            try:
                # call processTickets function
                module_zencheck.process_tickets()
                module_zencheck.process_tickets_es()
                # sleep for 600 seconds
                time.sleep(600)

            except Exception as er:
                print("{} - {}".format(__name__, er))
                continue

    except Exception as er:
        # only print the error, since module_log there isn't instance in main function
        print("{} - {}".format(__name__, er))
        # sleep 10 seconds and exit the application
        exit(1)


if __name__ == '__main__':
    # call function main
    main()
