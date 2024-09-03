from django.contrib import admin
from django.urls import path
from Apps.LaEsquina import views  # Asegúrate de importar la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Cambia a la vista de login
]
