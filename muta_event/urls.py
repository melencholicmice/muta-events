from django.contrib import admin
from django.urls import path
from user.urls import user_endpoints
from event.urls import event_endpoints
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(user_endpoints)),
    path('event/',include(event_endpoints))
]
