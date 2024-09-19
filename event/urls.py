from django.urls import path
from event.views import (
    CreateEvent,
    RegisterAttendee,
    GetEvent,
    GetAllEventsByUser,
    GetAllAttendeesByEvent
)

event_endpoints = [
    path("create-event", CreateEvent.as_view(), name="Department Login"),
    path("register-event/<uuid:event_id>",RegisterAttendee.as_view(), name="Add student to department"),
    path("get-event/<uuid:event_id>", GetEvent.as_view() ,name="Get Due by Id"),
    path("get-all-events-by-user", GetAllEventsByUser.as_view(), name="Get Dues"),
    path("get-all-attendees-by-event/<uuid:event_id>", GetAllAttendeesByEvent.as_view(), name="Get All Attendees by Event"),
]