# Generated by Django 2.1.1 on 2018-10-09 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bucketlist',
            name='date_modified',
        ),
    ]
