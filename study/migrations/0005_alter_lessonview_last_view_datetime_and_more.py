# Generated by Django 4.2.5 on 2023-10-07 14:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0004_alter_lesson_products_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonview',
            name='last_view_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 7, 14, 37, 37, 94876, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='lessonview',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='study.lesson'),
        ),
    ]
