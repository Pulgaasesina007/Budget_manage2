# Generated by Django 5.0 on 2023-12-23 05:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_module', '0007_ingresos_total_ingreso_alter_ingresos_fecha_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastos',
            name='fecha_registro',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='ingresos',
            name='fecha_registro',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
