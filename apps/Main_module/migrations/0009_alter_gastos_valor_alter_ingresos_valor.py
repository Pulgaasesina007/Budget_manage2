# Generated by Django 5.0 on 2023-12-27 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_module', '0008_alter_gastos_fecha_registro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastos',
            name='valor',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='ingresos',
            name='valor',
            field=models.FloatField(default=0.0),
        ),
    ]