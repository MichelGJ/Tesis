# Generated by Django 2.1.1 on 2019-03-23 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecciones', '0002_auto_20190223_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infotema',
            name='contenido',
        ),
        migrations.RemoveField(
            model_name='infotema',
            name='orden',
        ),
        migrations.AddField(
            model_name='infotema',
            name='presentacion',
            field=models.BooleanField(default=True),
        ),
    ]
