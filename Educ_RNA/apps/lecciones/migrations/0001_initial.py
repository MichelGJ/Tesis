# Generated by Django 2.1.1 on 2019-05-08 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoTema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentacion', models.BooleanField(default=True)),
                ('podcast', models.BooleanField(default=True)),
                ('codigo', models.BooleanField(default=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Leccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentacion', models.CharField(max_length=1024, null=True)),
                ('presentaciond', models.CharField(max_length=1024, null=True)),
                ('podcast', models.CharField(max_length=1024, null=True)),
                ('codigo', models.CharField(max_length=1024, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
