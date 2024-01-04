from django import forms
from django.contrib.auth.forms import  AuthenticationForm
from .models import user_perfil,Tipo_Gasto,Gastos,Tipo_Ingreso,Ingresos
class Register_User(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

    class Meta:
        model = user_perfil
        fields = ['username', 'password1', 'password2','nombres','correo','apellidos','telefono','fecha_nacimiento','cedula']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return password2




class Login_user(AuthenticationForm):
    username = forms.CharField
    password = forms.CharField(widget=forms.PasswordInput)
class act_password(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

# forms.py

class CambiarContraseñaForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Nueva contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

class Act_User(forms.ModelForm):
        class Meta:
            model = user_perfil
            fields = [ 'nombres', 'apellidos', 'cedula', 'telefono',  'correo']


#seccion de gastos e ingresos

class IngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        fields = ['tipoIngreso', 'descripcion', 'valor','fecha_registro']  # Excluye 'fecha_registro'

    tipoIngreso = forms.ModelChoiceField(
        queryset=Tipo_Ingreso.objects.all(),
        required=True,
        empty_label=None,

        widget=forms.Select(attrs={'style': 'width: 230px; height: 45px; font-size: 20px;'})
    )

class GastosForm(forms.ModelForm):
    class Meta:
        model = Gastos
        fields = ['tipoGasto', 'descripcion', 'valor','fecha_registro']  # Excluye 'fecha_registro'

    tipoGasto = forms.ModelChoiceField(
        queryset=Tipo_Gasto.objects.all(),
        required=True,
        empty_label=None,

        widget=forms.Select(attrs={'style': 'width: 230px; height: 45px; font-size: 20px;'})
    )