from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods


class GenerarMultaView(APIView):
    def get(self, request):
        # Obtén todos los préstamos que no han sido devueltos y cuya fecha y hora de vencimiento es antes de ahora
        prestamos_vencidos = Prestamo.objects.filter(devuelto=False)

        # Para cada préstamo vencido, crea una nueva multa
        for prestamo in prestamos_vencidos:
            multa = Multa.objects.create(prestamo=prestamo)
            multa.generar_multa()

        return Response({"message": "Multas generadas exitosamente"})
    
#class Multas_generadas_dia(APIView):
@require_http_methods(["GET"])
def multas_por_dia(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)

    multas_por_dia = Multa.objects.filter(
            fecha_hora_generacion__range=(fecha_inicio, fecha_fin)
        ).values('fecha_hora_generacion__date').annotate(total_multas=Sum('monto'))

    data = list(multas_por_dia)
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def articulos_prestados_por_dia(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)

    articulos_prestados_por_dia = Prestamo.objects.filter(
        fecha_hora_prestamo__range=(fecha_inicio, fecha_fin)
    ).values('fecha_hora_prestamo__date').annotate(cantidad=Count('id'))

    data = list(articulos_prestados_por_dia)
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def articulos_prestados_por_deporte(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)

    articulos_prestados_por_deporte = Prestamo.objects.filter(
        fecha_hora_prestamo__range=(fecha_inicio, fecha_fin)
    ).values('articulo_deportivo__deporte').annotate(cantidad=Count('id'))

    data = list(articulos_prestados_por_deporte)
    return JsonResponse(data, safe=False)
