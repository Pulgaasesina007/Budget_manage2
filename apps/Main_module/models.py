from django.db import models,transaction
from django.contrib.auth.models import AbstractUser
from django.db.models import  Sum
from django.utils import timezone


# Create your models here.

class user_perfil(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    nombres = models.CharField(max_length=100, null=True)
    apellidos = models.CharField(max_length=100, null=True )
    cedula = models.CharField(max_length=10, null=True)
    telefono = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField(null=True)
    correo = models.EmailField(null=True)



    OPCIONES_ROL = [
        ('usuario', 'Usuario normal'),
        ('admin', 'Administrador'),
    ]
    roles = models.CharField(max_length=7, choices=OPCIONES_ROL, default='usuario')
    def __str__(self):
        return self.username

class Tipo_Ingreso(models.Model):

    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.nombre}'

class Ingresos(models.Model):

    descripcion = models.TextField()
    fecha_registro = models.DateField(null=True, default=timezone.now)
    valor = models.FloatField(default=0.0)
    tipoIngreso = models.ForeignKey(Tipo_Ingreso, on_delete=models.PROTECT)
    Usuario = models.ForeignKey(user_perfil, on_delete=models.CASCADE)
    total_ingreso = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Calcular el total de gastos para el mismo tipoGasto
            tipo_ingreso_actual = self.tipoIngreso
            ingreso_con_mismo_tipo = Ingresos.objects.filter(tipoIngreso=tipo_ingreso_actual)
            total_ingreso_tipo_actual = ingreso_con_mismo_tipo.aggregate(Sum('valor'))['valor__sum'] or 0.0

            # Actualizar el total_gasto
            self.total_ingreso = total_ingreso_tipo_actual + self.valor

            # Guardar el nuevo registro
            super().save(*args, **kwargs)


class Tipo_Gasto(models.Model):

    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Gastos(models.Model):

    descripcion = models.TextField()
    fecha_registro = models.DateField(null=True, default=timezone.now)
    valor = models.FloatField(default=0.0)
    tipoGasto = models.ForeignKey(Tipo_Gasto, on_delete=models.PROTECT,null=True)
    Usuario = models.ForeignKey(user_perfil, on_delete=models.CASCADE)
    total_gasto = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Calcular el total de gastos para el mismo tipoGasto
            tipo_gasto_actual = self.tipoGasto
            gastos_con_mismo_tipo = Gastos.objects.filter(tipoGasto=tipo_gasto_actual)
            total_gasto_tipo_actual = gastos_con_mismo_tipo.aggregate(Sum('valor'))['valor__sum'] or 0.0

            # Actualizar el total_gasto
            self.total_gasto = total_gasto_tipo_actual + self.valor

            # Guardar el nuevo registro
            super().save(*args, **kwargs)