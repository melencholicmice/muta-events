from django.db import models
from utils.enum_mixin import EnumMixin
from uuid import uuid4
from core.db.timestamp_mixin import TimestampMixin

class SubscriptionEnum(EnumMixin):
    BASIC = 'basic', 'Basic Plan'
    PREMIUM = 'premium', 'Premium Plan'


class User(TimestampMixin):

    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid4, 
        editable=False
    )

    first_name = models.CharField(max_length=150)

    last_name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)

    is_email_verified = models.BooleanField(default=False)

    password = models.CharField(max_length=255)

    subscription = models.CharField(
        max_length=10,
        choices=SubscriptionEnum.choices(),
        default=SubscriptionEnum.BASIC.internal
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

