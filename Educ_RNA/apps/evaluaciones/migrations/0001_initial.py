# Generated by Django 2.1.1 on 2019-02-24 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lecciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Prueba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('modelo', models.IntegerField()),
                ('id_leccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecciones.Leccion')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecciones.Leccion')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(max_length=120)),
                ('respuestacorrecta', models.BooleanField()),
                ('id_pregunta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.Pregunta')),
            ],
        ),
        migrations.AddField(
            model_name='pregunta',
            name='id_prueba',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.Prueba'),
        ),
        migrations.AddField(
            model_name='pregunta',
            name='id_quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.Quiz'),
        ),
    ]
