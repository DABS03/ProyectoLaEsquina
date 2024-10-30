import re
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Rol, Producto, CategoriaProducto
from django.core.exceptions import ValidationError


class CrearCuentaForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput())
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')
    telefono = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}))

    class Meta:
        model = Usuario
        fields = ['nombres', 'usuario', 'contrasena', 'confirmar_contrasena', 'correo', 'telefono', 'direccion']

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        # Verificar que solo contenga letras
        if not re.match(r'^[a-zA-Z\s]+$', nombres):
            raise ValidationError('El nombre solo puede contener letras y espacios.')
        
        return nombres

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono').strip()

        # Verificación teléfono de 8 dígitos
        if not telefono.isdigit() or len(telefono) != 8:
            raise ValidationError('El teléfono debe ser un número entero de 8 dígitos.')
        
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data.get('correo').strip()

        # Verificar si el correo tiene la estructura correcta
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
            raise ValidationError('El correo debe tener el formato nombre@correo.com.')
        
        return correo

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')

        # Eliminar todos los espacios 
        usuario = usuario.replace(' ', '')

        # Verificar que no haya mayúsculas en el usuario
        if any(char.isupper() for char in usuario):
            raise ValidationError('El usuario no debe contener letras mayúsculas.')
        
        return usuario


    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")

        # Verificar que las contraseñas coincidan
        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            self.add_error('confirmar_contrasena', 'Las contraseñas no coinciden.')
        return cleaned_data

def agregar_producto(request):
    categorias = CategoriaProducto.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')  # Cambiado a 'nombre'
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        categoria_id = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')  # Si la imagen es opcional, maneja su valor

        # Validación para asegurar que los campos obligatorios no estén vacíos
        if not all([nombre, precio, cantidad, categoria_id, descripcion]):
            messages.error(request, 'Por favor, complete todos los campos obligatorios.')
            return render(request, 'agregar_pro.html', {'categorias': categorias})

        try:
            # Obtener la categoría seleccionada
            categoria = CategoriaProducto.objects.get(id_categoria_producto=categoria_id)
            
            # Crear el producto
            producto = Producto(
                nombre_producto=nombre,
                precio=precio,
                cantidad_stock=cantidad,
                descripcion=descripcion,
                id_categoria_producto=categoria,
                imagen=imagen  # Asigna la imagen si está presente
            )
            producto.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('ver_inventario')  # Redirige a la vista del inventario
        except CategoriaProducto.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe.')

    return render(request, 'agregar_pro.html', {'categorias': categorias})

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'precio', 'cantidad_stock', 'id_categoria_producto', 'descripcion', 'imagen']
        
        labels = {
            'nombre_producto': 'Nombre',
            'precio': 'Precio',
            'cantidad_stock': 'Cantidad',
            'id_categoria_producto': 'Categoría',
            'descripcion': 'Descripción',
            'imagen': 'Imagen',
        }
        
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
        