# Generated by Django 2.1.1 on 2019-05-23 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
