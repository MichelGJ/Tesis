# Generated by Django 2.1.1 on 2018-10-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_bucketlist_date_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucketlist',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
