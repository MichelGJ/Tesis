# Generated by Django 2.1.1 on 2019-05-23 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190523_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progreso',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='P_U_FK', to=settings.AUTH_USER_MODEL),
        ),
    ]