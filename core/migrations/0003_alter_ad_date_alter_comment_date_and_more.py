# Generated by Django 4.0.1 on 2023-01-11 20:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_comment_date_commentreplay_comment_replaies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='commentreplay',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
