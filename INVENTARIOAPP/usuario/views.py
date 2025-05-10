from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    rol = request.user.perfil.rol.nombre if hasattr(request.user, 'perfil') and request.user.perfil.rol else 'Sin rol'
    return render(request, 'inicio.html', {'rol': rol})

class FormularioLogin(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class InicioSesionView(LoginView):
    template_name = 'login.html'
    authentication_form = FormularioLogin
    redirect_authenticated_user = True
    success_url = reverse_lazy('inicio')


