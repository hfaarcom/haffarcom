# Generated by Django 4.0.1 on 2023-01-29 14:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_ad_photo_alter_product_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='photo',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 29, 17, 11, 16, 619001, tzinfo=utc), null=True),
        ),
    ]
