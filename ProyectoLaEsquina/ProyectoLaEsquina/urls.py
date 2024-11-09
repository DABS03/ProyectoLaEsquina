from django.contrib import admin
from django.urls import path, include
from Apps.LaEsquina import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('crear-cuenta/', views.crear_cuenta, name='crear_cuenta'),

    # Admin
    path('admin_view/', views.admin_view, name='admin_view'),
    path('edit_pro/<int:producto_id>/', views.edit_pro, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('agregar-pro/', views.agregar_pro, name='agregar_pro'),
    path('inventario/', views.ver_inventario, name='ver_inventario'),
    path('historial_pedidos/',views.historial_pedidos, name='historial_pedidos'),
    path('cambiar_estado/<int:pedido_id>/', views.cambiar_estado, name='cambiar_estado'),
    path('historial_solicitudes/',views.historial_solicitudes, name='historial_solicitudes'),
    path('cambiar_estado_solicitud/<int:pedido_id>/', views.cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
    #path('enviar_pedido/', views.enviar_pedido, name='enviar_pedido'),


    # Aseguradora
    path('aseguradora_view/', views.aseguradora_view, name='aseguradora_view'),
    path('crear_pedido_servicio/', views.crear_pedido_servicio, name='crear_pedido_servicio'),

    #Google
    path('auth/', include('allauth.urls')),
    path('google_login/', views.google_login, name='google_login'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),

    # Cliente
        #todos la pueden ver
    path('cliente_view/', views.cliente_view, name='cliente_view'), 
    path('v_producto/<int:producto_id>/', views.producto_view, name='v_producto'),
        ####################
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('mi_carrito/', views.mi_carrito_view, name='mi_carrito'),
    path('eliminar_del_carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('enviar_sugerencia/', views.enviar_sugerencia, name='enviar_sugerencia'),

    #Pedidos
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido_realizado/', views.pedido_realizado, name='pedido_realizado'),
    path('update_direccion/', views.update_direccion, name='update_direccion'),
    path('pedido_exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    path('enviar_comentario/<int:pedido_id>/', views.enviar_comentario, name='enviar_comentario'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)