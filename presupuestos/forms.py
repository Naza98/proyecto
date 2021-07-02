from django import forms
from django.forms import widgets
from presupuestos.models import Presupuesto
from fac.models import Cliente

class PresupuestosForm(forms.ModelForm):

    plazo = forms.DateField(required=True,
    widget=widgets.NumberInput(attrs=({'type' : 'date',
                                        'class':'form-control'})))

    fecha = forms.DateField(required=True,
    widget=widgets.NumberInput(attrs=({'type' : 'date',
                                        'class':'form-control'})))

    class Meta:
        model=Presupuesto

        fields=[
            'cliente',
            'producto',
            'precio_unitario',
            'cantidad',
            'total',
            'plazo',
            'fecha'
        ]
        labels={
            'cliente': 'Cliente',
            'producto': 'Producto',
            'precio_unitario': 'Precio unitario',
            'cantidad': 'Cantidad',
            'total': 'Total',
            'plazo': 'Plazo Hasta',
            'fecha':'Fecha de Emisión'
        }
        widgets={
            'cliente': forms.Select(attrs=({'class': 'form-control'})),  
            'producto': forms.Select(attrs={'class':'form-control'}), #'onchange':'cambioSelect();'
            'precio_unitario': forms.TextInput(attrs={'class':'form-control'}),
            'cantidad': forms.TextInput(attrs={'class':'form-control'}),
            'total': forms.TextInput(attrs={'class':'form-control' })
        }
