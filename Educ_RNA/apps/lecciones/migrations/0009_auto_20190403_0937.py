# Generated by Django 2.1.1 on 2019-04-03 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecciones', '0008_auto_20190403_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infotema',
            name='tema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lecciones.Tema'),
        ),
    ]
