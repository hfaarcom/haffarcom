# Generated by Django 4.0.1 on 2023-01-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uudi',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
