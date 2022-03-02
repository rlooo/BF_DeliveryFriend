"""
WSGI config for deliveryFriend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from gunicorn import app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deliveryFriend.settings')

application = get_wsgi_application()

port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=port, debug=True)

