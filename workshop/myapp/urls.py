from django.urls import path
from .views import GenerarMultaView#, Multas_generadas_dia
from . import views


urlpatterns = [
    #path('multas-por-dia/', Multas_generadas_dia.as_view(), name='multas-por-dia'),
    path('multas-por-dia/', views.multas_por_dia, name='multas-por-dia'),
    path('articulos-prestados-por-dia/', views.articulos_prestados_por_dia, name='articulos-prestados-por-dia'),
    path('articulos-prestados-por-deporte/', views.articulos_prestados_por_deporte, name='articulos-prestados-por-deporte'),
    path('generar_multas/', GenerarMultaView.as_view(), name='generar_multas'),
]

#http://127.0.0.1:8000/myapp/multas-por-dia/?fecha_inicio=2023-10-01&fecha_fin=2023-10-01 
#http://127.0.0.1:8000/myapp/articulos-prestados-por-dia/?fecha_inicio=2023-10-01&fecha_fin=2023-10-01
#http://127.0.0.1:8000/myapp/articulos-prestados-por-deporte/?fecha_inicio=2023-10-01&fecha_fin=2023-10-01