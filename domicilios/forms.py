from django import forms

#from .models import Domicilio

from fac.models import Cliente

from .models import Provincia, Localidad, Barrio
 
'''
class DomicilioForm(forms.ModelForm):

    provincia = forms.CharField(max_length=300, required=True, 
    widget=forms.Select(attrs=({'class' : 'form-control form-control-sm'})))


    localidad = forms.CharField(max_length=300, required=True, 
    widget=forms.Select(attrs=({'class' : 'form-control'})))

    barrio = forms.ModelChoiceField(queryset=Barrio.objects.all())

    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=forms.HiddenInput())

    calle = forms.CharField(max_length=300, required=True, 
    widget=forms.TextInput(attrs=({'class' : 'form-control'})))

    altura = forms.CharField(max_length=300, required=True, 
    widget=forms.TextInput(attrs=({'class' : 'form-control'})))

    manzana = forms.CharField(max_length=300, required=False, 
    widget=forms.TextInput(attrs=({'class' : 'form-control'})))

    departamento = forms.CharField(max_length=300, required=False, 
    widget=forms.TextInput(attrs=({'class' : 'form-control'})))

    piso = forms.CharField(max_length=300, required=False, 
    widget=forms.TextInput(attrs=({'class' : 'form-control'})))

    observacion = forms.CharField(max_length=300, required=False, 
    widget=forms.TextInput(attrs=({'class' : 'form-control'})))

    class Meta: 
        fields = [ 'provincia',
                    'localidad',
                    'barrio',
                'cliente',
                 'calle',
                 'altura',
                 'manzana',
                 'departamento',
                 'piso',
                 'observacion']
        model = Domicilio
'''