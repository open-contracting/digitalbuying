#!/usr/bin/env python
import os
import sys
import dotenv

if __name__ == "__main__":

    try:
        dotenv.read_dotenv()
    except FileNotFoundError:
        pass
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ictcg.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)