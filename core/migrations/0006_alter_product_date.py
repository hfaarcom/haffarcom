# Generated by Django 4.0.1 on 2023-01-21 12:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_product_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
