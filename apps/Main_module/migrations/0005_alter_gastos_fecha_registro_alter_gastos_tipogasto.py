# Generated by Django 5.0 on 2023-12-22 05:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_module', '0004_gastos_total_gasto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastos',
            name='fecha_registro',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='gastos',
            name='tipoGasto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Main_module.tipo_gasto'),
        ),
    ]
