from django.contrib import admin
from django.urls import path
from user.urls import user_endpoints
from event.urls import event_endpoints
from django.urls import include
from core.stripe_plugin import stripe_webhook_handler
from utils.api_lister_view import list_api

urlpatterns = [
    path('',list_api),
    path('admin/', admin.site.urls),
    path('user/',include(user_endpoints)),
    path('event/',include(event_endpoints)),
    path('webhook', stripe_webhook_handler, name='stripe_webhook'),
]
