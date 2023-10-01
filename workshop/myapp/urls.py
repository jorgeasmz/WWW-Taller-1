from django.urls import path
from .views import GenerarMultaView

urlpatterns = [
    path('generar_multas/', GenerarMultaView.as_view(), name='generar_multas'),
]