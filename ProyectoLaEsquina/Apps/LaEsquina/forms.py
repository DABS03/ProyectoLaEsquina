from django import forms
from .models import Usuario, Rol

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
