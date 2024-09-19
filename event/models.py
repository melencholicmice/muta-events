from django.db import models
from uuid import uuid4
from user.models import User
from core.db.timestamp_mixin import TimestampMixin

class Event(TimestampMixin):

    event_id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )

    name = models.CharField(max_length=255)

    description = models.TextField()

    location = models.CharField(max_length=255)

    is_bought = models.BooleanField(default=False)

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )


class EventAttendee(TimestampMixin):
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='attendees'
    )

    name = models.CharField(max_length=255)

    phone_number = models.CharField(
        max_length=10, 
    )

    email = models.EmailField()
