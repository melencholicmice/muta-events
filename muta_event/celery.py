# # backend/celery.py
# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# # Set the default Django settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muta_event.settings')

# app = Celery('muta_event')

# # Load configuration from Django settings, using a CELERY namespace
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Auto-discover tasks from installed apps
# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
