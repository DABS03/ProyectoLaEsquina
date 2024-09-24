from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, Rol, Producto, CategoriaProducto

class CrearCuentaForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput())
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')
    telefono = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}))

    class Meta:
        model = Usuario
        fields = ['nombres', 'usuario', 'contrasena', 'confirmar_contrasena', 'correo', 'telefono', 'direccion']

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")
        # Contraseñas deben ser iguales
        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            self.add_error('confirmar_contrasena', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asignar el rol de cliente a todos los usuarios creados
        rol_cliente = Rol.objects.get(nombre_rol='Cliente')
        user.id_rol = rol_cliente
        # Asignar la contraseña directamente sin cifrar
        user.contrasena = self.cleaned_data['contrasena']
        if commit:
            user.save()
        return user



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