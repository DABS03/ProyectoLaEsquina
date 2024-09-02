from django.db import models

#Base de datos LaEsquina

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.PositiveIntegerField()
    direccion = models.CharField(max_length=255)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)
    imagen = models.BinaryField(null=True, blank=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario

class EstadoPedido(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_estado

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField()
    fecha_entrega = models.DateField()
    comentarios = models.TextField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    id_estado = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.fecha_pedido}"

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre_servicio

class PedidoServicio(models.Model):
    id_pedido_servicio = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id_pedido.id_pedido} - Servicio {self.id_servicio.nombre_servicio}"

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    cantidad_stock = models.PositiveIntegerField()
    imagen = models.BinaryField(null=True, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    id_categoria_producto = models.ForeignKey('CategoriaProducto', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_producto

class CategoriaProducto(models.Model):
    id_categoria_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class PedidoProducto(models.Model):
    id_pedido_producto = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id_pedido.id_pedido} - Producto {self.id_producto.nombre_producto}"

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre_proveedor

class SolicitudStock(models.Model):
    id_solicitudStock = models.AutoField(primary_key=True)
    plantilla = models.CharField(max_length=100)
    fecha_solicitud = models.DateField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Solicitud {self.id_solicitudStock} - Producto {self.id_producto.nombre_producto}"

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito {self.id_carrito} - Usuario {self.id_usuario.usuario}"

class ItemsCarrito(models.Model):
    id_itemsCarrito = models.AutoField(primary_key=True)
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Carrito {self.id_carrito.id_carrito} - Producto {self.id_producto.nombre_producto}"
