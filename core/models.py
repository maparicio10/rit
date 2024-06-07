import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Nombres")
    last_name = models.CharField(max_length=50, verbose_name="Apellidos")
    email = models.EmailField(max_length=100, verbose_name="Correo electrónico")

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.fullname


class Officer(User):
    identification_number = models.BigIntegerField(unique=True, null=False, editable=False,
                                                   verbose_name="Número de identificación")

    class Meta:
        verbose_name = "Oficial"
        verbose_name_plural = "Oficiales"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.identification_number is None:
            self.identification_number = uuid.uuid4().int % 10 ** 10

        # if not self.pk or 'password' in kwargs:
        #     self.set_password(self.password)

        super().save(*args, **kwargs)


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=25, unique=True, verbose_name="Placa de patente")
    brand = models.CharField(max_length=50, verbose_name="Marca")
    color = models.CharField(max_length=25, verbose_name="Color")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Dueño/a")

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"{self.license_plate} - {self.brand} - {self.color}"


class Violation(models.Model):
    timestamp = models.DateTimeField(verbose_name="Fecha y hora")
    comments = models.TextField(verbose_name="Comentarios")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Vehículo")
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, verbose_name="Oficial")

    class Meta:
        verbose_name = "Infracción"
        verbose_name_plural = "Infracciones"

    def __str__(self):
        return f"Violation {self.id} - {self.timestamp}"
