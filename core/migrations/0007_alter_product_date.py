# Generated by Django 4.0.1 on 2023-01-21 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_product_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.date(2023, 1, 21), null=True),
        ),
    ]
