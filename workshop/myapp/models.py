from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time

class Univalluno(models.Model):
    
    class Meta:
        unique_together = (('tipo_documento', 'numero_documento'),)

    # Campos para los univallunos
    tipo_documento = models.CharField(max_length=2, choices=[('CC', 'Cédula de Ciudadanía'), ('TI', 'Tarjeta de Identidad')])
    numero_documento = models.CharField(max_length=20)
        
    # Campos restantes
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    codigo_estudiante = models.CharField(max_length=20, blank=True, null=True, unique=True)
    correo_electronico = models.EmailField(unique=True)
    tipo_univalluno = models.CharField(max_length=20, choices=[("Estudiante", "Estudiante"), ("Funcionario", "Funcionario")])

    def __str__(self):
        return self.numero_documento

class ArticuloDeportivo(models.Model):
    # Campos para los artículos deportivos
    nombre = models.CharField(max_length=100)
    deporte = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)  # Por defecto, el artículo está disponible

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    # Campos para los préstamos
    univalluno = models.ForeignKey(Univalluno, on_delete=models.CASCADE)
    articulo_deportivo = models.ForeignKey(ArticuloDeportivo, on_delete=models.CASCADE)
    fecha_hora_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_hora_vencimiento = models.DateTimeField()
    devuelto = models.BooleanField(default=False)  # Por defecto, el artículo no ha sido devuelto

    def clean(self):
        # Verificar si el Univalluno ya tiene un préstamo
        if Prestamo.objects.filter(univalluno=self.univalluno).exists():
            raise ValidationError('Un Univalluno solo puede tener un préstamo a la vez.')

    def save(self, *args, **kwargs):
        # Establece fecha_hora_prestamo a la hora actual
        now = datetime.now()
        self.fecha_hora_prestamo = timezone.make_aware(now)

        # Establece fecha_hora_vencimiento a las 8:00 PM del día actual
        self.fecha_hora_vencimiento = timezone.make_aware(datetime.combine(now.date(), time(20, 0)))

        # Marca el artículo deportivo como no disponible
        self.articulo_deportivo.disponible = False
        self.articulo_deportivo.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.univalluno.nombres + " - " + self.articulo_deportivo.nombre

class Multa(models.Model):
    # Campos para las multas
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    fecha_hora_generacion = models.DateTimeField(auto_now_add=True)
    fecha_hora_pago = models.DateTimeField(null=True, blank=True)  # Campo para registrar la fecha-hora de pago
    monto = models.IntegerField(null=True, blank=True)
    multa_pagada = models.BooleanField(default=False)  # Por defecto, la multa no ha sido pagada

    def calcular_monto_multa(self):
        # Calcular la multa diaria como el 15% del valor del artículo diario
        valor_articulo = int(self.prestamo.articulo_deportivo.valor)
        dias_atraso = (timezone.now() - self.prestamo.fecha_hora_vencimiento).days
        monto_multa = valor_articulo * 0.15 * dias_atraso
        return int(monto_multa)  # Redondear el monto a un número entero

    def generar_multa(self):
        if not self.multa_pagada:
            self.monto = self.calcular_monto_multa()
            self.save()

    def pagar_multa(self):
        self.fecha_hora_pago = timezone.now()
        self.multa_pagada = True
        self.prestamo.devuelto = True
        self.prestamo.save()
        self.prestamo.articulo_deportivo.disponible = True
        self.prestamo.articulo_deportivo.save()
        self.save()
    
    def __str__ (self):
        return self.prestamo.univalluno.nombres
