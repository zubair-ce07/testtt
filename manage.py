#!/usr/bin/env python
import os
import sys
import eproperty_api.settings

if __name__ == "__main__":

    os.environ['DJANGO_SETTINGS_MODULE'] = 'eproperty_api.settings'
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
