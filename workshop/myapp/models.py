from django.db import models
from datetime import datetime, time, timedelta

class Univalluno(models.Model):
    # Campos para los univallunos
    tipo_documento = models.CharField(max_length=2, choices=[('CC', 'Cédula de Ciudadanía'), ('TI', 'Tarjeta de Identidad')])
    numero_documento = models.CharField(max_length=20)
    
    class Meta:
        # Establece una restricción única para la combinación de Tipo de documento y Número de documento
        unique_together = ('tipo_documento', 'numero_documento')
    
    # Campos restantes
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    codigo_estudiante = models.CharField(max_length=20, blank=True, null=True, unique=True)
    correo_electronico = models.EmailField(unique=True)
    tipo_univalluno = models.CharField(max_length=20, choices=[("Estudiante", "Estudiante"), ("Funcionario", "Funcionario")])
    prestamo_activo = models.BooleanField(default=False)  # Por defecto, el Univalluno no tiene un préstamo activo

class ArticuloDeportivo(models.Model):
    # Campos para los artículos deportivos
    nombre = models.CharField(max_length=100)
    deporte = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)  # Por defecto, el artículo está disponible

class Prestamo(models.Model):
    # Campos para los préstamos
    univalluno = models.ForeignKey(Univalluno, on_delete=models.CASCADE)
    articulo_deportivo = models.ForeignKey(ArticuloDeportivo, on_delete=models.CASCADE)
    fecha_hora_prestamo = models.DateTimeField(auto_now_add=True)
    # Fecha-hora de vencimiento (se calcula automáticamente a las 8:00 PM del mismo día)
    def calcular_fecha_hora_vencimiento(self):
        now = datetime.now()
        hora_vencimiento = time(20, 0, 0)  # Hora de vencimiento a las 8:00 PM
        fecha_hora_vencimiento = datetime.combine(now.date(), hora_vencimiento)
        if now.time() >= hora_vencimiento:
            # Si la hora actual es después de las 8:00 PM, se agrega un día
            fecha_hora_vencimiento += timedelta(days=1)
        return fecha_hora_vencimiento
    
    fecha_hora_vencimiento = models.DateTimeField(default=calcular_fecha_hora_vencimiento)
    multa_pagada = models.BooleanField(default=False)

class Multa(models.Model):
    # Campos para las multas
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    fecha_hora_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=0)

    def calcular_monto_multa(self):
        # Calcula el monto de la multa como el 15% del valor del artículo por día
        valor_articulo = self.prestamo.articulo_deportivo.valor
        fecha_prestamo = self.prestamo.fecha_hora_prestamo.date()
        fecha_devolucion = self.prestamo.fecha_hora_vencimiento.date()
        dias_en_prestamo = (fecha_devolucion - fecha_prestamo).days + 1  # Suma 1 para incluir el día de préstamo
        monto_multa = valor_articulo * 0.15 * dias_en_prestamo
        return monto_multa
    
    def save(self, *args, **kwargs):
        if not self.monto:
            self.monto = self.calcular_monto_multa()
        super(Multa, self).save(*args, **kwargs)
