# Generated by Django 4.0.1 on 2023-01-26 16:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 26, 19, 47, 30, 668388, tzinfo=utc), null=True),
        ),
    ]
