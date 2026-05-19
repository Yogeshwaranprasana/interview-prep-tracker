"""
WSGI config for mytracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
import time

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytracker.settings')

# Apply any pending migrations on startup to avoid missing auth_user/table errors.
# Retry a few times so the app can start when the database is still warming up.
try:
    from django.core.management import call_command
    from django.db.utils import OperationalError

    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            call_command('migrate', interactive=False, run_syncdb=True)
            break
        except OperationalError as exc:
            if attempt == max_retries:
                raise
            sys.stderr.write(
                f'Warning: database unavailable on attempt {attempt}, retrying...\n'
            )
            time.sleep(3)
except Exception as exc:
    sys.stderr.write(f'Warning: automatic migrate failed: {exc}\n')

application = get_wsgi_application()
