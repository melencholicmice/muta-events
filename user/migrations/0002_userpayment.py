# Generated by Django 5.1.1 on 2024-09-20 09:41

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPayment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_boolean', models.BooleanField(default=False)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stripe_checkout_session_id', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_payments', to='user.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
