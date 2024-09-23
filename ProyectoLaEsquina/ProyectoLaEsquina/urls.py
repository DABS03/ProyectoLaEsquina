from django.contrib import admin
from django.urls import path
from Apps.LaEsquina import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('cliente_view/', views.cliente_view, name='cliente_view'),
    path('aseguradora_view/', views.aseguradora_view, name='aseguradora_view'),
    path('crear-cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('inventario/', views.ver_inventario, name='ver_inventario'),
    path('v_producto/<int:producto_id>/', views.producto_view, name='v_producto'),
    path('agregar-pro/', views.agregar_pro, name='agregar_pro'),
    path('logout/', views.logout_view, name='logout'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
