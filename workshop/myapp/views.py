from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa
from django.utils import timezone

class GenerarMultaView(APIView):
    def get(self, request):
        # Obtén todos los préstamos que no han sido devueltos y cuya fecha y hora de vencimiento es antes de ahora
        prestamos_vencidos = Prestamo.objects.filter(devuelto=False)

        # Para cada préstamo vencido, crea una nueva multa
        for prestamo in prestamos_vencidos:
            multa = Multa.objects.create(prestamo=prestamo)
            multa.generar_multa()

        return Response({"message": "Multas generadas exitosamente"})