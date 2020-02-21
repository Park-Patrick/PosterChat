"""
WSGI config for posterchat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/ROBARTS/ppark/Documents/PosterChat')
sys.path.append('/home/ROBARTS/ppark/Documents/PosterChat/venv/lib/python3.7/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posterchat.settings')

application = get_wsgi_application()
