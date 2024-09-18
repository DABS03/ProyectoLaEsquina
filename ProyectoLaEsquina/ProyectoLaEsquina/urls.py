from django.contrib import admin
from django.urls import path
from Apps.LaEsquina import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('cliente_view/', views.cliente_view, name='cliente_view'),
    path('aseguradora_view/', views.aseguradora_view, name='aseguradora_view'),
    path('crear-cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('inventario/', views.ver_inventario, name='ver_inventario'),
] 
