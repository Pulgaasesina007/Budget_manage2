# Generated by Django 5.0 on 2023-12-16 00:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_module', '0002_alter_user_perfil_apellidos_alter_user_perfil_cedula_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_Gasto',
            fields=[
                ('idTipoGasto', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Ingreso',
            fields=[
                ('idTipoIngreso', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('idgasto', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('descripcion', models.TextField()),
                ('fecha_registro', models.DateTimeField(auto_now=True)),
                ('valor', models.FloatField()),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipoGasto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Main_module.tipo_gasto')),
            ],
        ),
        migrations.CreateModel(
            name='Ingresos',
            fields=[
                ('idingreso', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('descripcion', models.TextField()),
                ('fecha_registro', models.DateTimeField(auto_now=True)),
                ('valor', models.FloatField()),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipoIngreso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Main_module.tipo_ingreso')),
            ],
        ),
    ]
