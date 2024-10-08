# Generated by Django 5.1.1 on 2024-09-19 06:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('is_bought', models.BooleanField(default=False)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organized_events', to='user.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventAttendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to='event.event')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
