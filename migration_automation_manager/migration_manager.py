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
from migration_automation_manager.module_consume import ModuleConsume
import time


def main():
    """
    **Main function, this instance ModuleConsume class and call consume function.**
    Error generate a exit with code 1.
    """
    try:
        # create ModuleConsume instance
        module_consume = ModuleConsume("manager")
        # call consume function
        module_consume.consume()

    except Exception as er:
        # only print the error, since moduleLog there isn't instance in main function
        print("{} - {}".format(__name__, er))
        # sleep 10 seconds and exit the application
        time.sleep(10)
        exit(1)


if __name__ == '__main__':
    # call function main
    main()
