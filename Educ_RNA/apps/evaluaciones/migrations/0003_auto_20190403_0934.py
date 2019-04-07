# Generated by Django 2.1.1 on 2019-04-03 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluaciones', '0002_auto_20190223_2306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respuesta',
            old_name='respuestacorrecta',
            new_name='correcta',
        ),
        migrations.RemoveField(
            model_name='prueba',
            name='modelo',
        ),
        migrations.RemoveField(
            model_name='prueba',
            name='nombre',
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='contenido',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='prueba',
            name='leccion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lecciones.Leccion'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='tema',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='lecciones.Tema'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='contenido',
            field=models.CharField(max_length=320),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluaciones.Pregunta'),
        ),
    ]
