from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MaxLengthValidator
from HeroSound.models import Cancion, Perfil

class FormUser(forms.Form):
    name = forms.CharField(validators=[MaxLengthValidator(5)])
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput)
    
    def clean_botcatcher(self):
        atrapador = self.cleaned_data['botcatcher']
        if len(atrapador) > 0:
            raise forms.ValidationError("Ese mi EL BOT!")
        return atrapador

class RegistroForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150, help_text='')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener el tipo de usuario enviado en los argumentos del formulario
        tipo_usuario = kwargs.get('initial', {}).get('tipo_usuario')
        # Condición para mostrar las opciones dependiendo del tipo de usuario
        if tipo_usuario == 'administrador':
            # Opciones para el tipo de usuario administrador
            self.fields['tipo_usuario'] = forms.ChoiceField(choices=(('user', 'User'), ('administrador', 'Administrador')))
        else:
            # Opciones para el tipo de usuario normal
            self.fields['tipo_usuario'] = forms.ChoiceField(choices=(('user', 'User'),))

    class Meta:
        model = Perfil
        fields = ['username', 'password', 'tipo_usuario']
        
class FormularioCancion(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = ['titulo', 'artista', 'archivo_mp3', 'imagen']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )
