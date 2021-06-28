from typing import Pattern
from django import forms
from django.forms import ValidationError
from django.forms.widgets import NumberInput
from .models import Cliente


class ClienteForm(forms.ModelForm):    

    class Meta:
        model=Cliente
        fields=['nombres','apellidos', 'tipo_documento' ,'numero_dni', 'fecha_nacimiento', 'sexo','tipo',
            'celular', 'email', 'barrio', 'calle', 'altura', 'manzana', 'departamento', 'piso', 'observacion', 'estado']
        exclude = ['um','fm','uc','fc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


    fecha_nacimiento = forms.DateField(required=True,
    widget=NumberInput(attrs=({'type' : 'date'})))

    celular = forms.CharField(required=True,
    widget=NumberInput())

    def clean_celular(self):
        celular = self.cleaned_data['celular']
        if int(celular) < 0:
            raise ValidationError("Este campo no puede contener valores negativos")
        return celular  

    numero_dni = forms.IntegerField(required=True,
        widget=forms.NumberInput(attrs=({'placeholder':'Ingrese el numero sin puntos, ni espacios'})))

    def clean_numero_dni(self):
        numero_dni = self.cleaned_data['numero_dni']
        if numero_dni < 0:
            raise ValidationError("Este campo no puede contener valores negativos")
        return numero_dni  