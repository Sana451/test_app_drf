# Generated by Django 4.2.5 on 2023-10-06 05:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_lessonview_last_time_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonview',
            name='last_time_datetime',
        ),
        migrations.AddField(
            model_name='lessonview',
            name='last_view_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 6, 5, 14, 56, 861442, tzinfo=datetime.timezone.utc)),
        ),
    ]
