#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
    if not settings_module:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'testsettings'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
