"""
WSGI config for mytracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytracker.settings')

# Apply any pending migrations on startup. This prevents errors like
# "relation auth_user does not exist" when the database has not been migrated.
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False, run_syncdb=True)
except Exception as exc:
    sys.stderr.write(f'Warning: automatic migrate failed: {exc}\n')

application = get_wsgi_application()
