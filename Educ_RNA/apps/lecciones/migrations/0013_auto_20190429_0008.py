# Generated by Django 2.1.1 on 2019-04-29 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecciones', '0012_auto_20190429_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infotema',
            name='tema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lecciones.Tema', unique=True),
        ),
    ]