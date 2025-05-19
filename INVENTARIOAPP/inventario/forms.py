from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['responsable']
        fields = '__all__'
    imagen = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
