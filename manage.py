#!/usr/bin/env python
import os, sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tani_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Install Django dulu: pip install django") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
