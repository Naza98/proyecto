from django import forms

from .models import Proveedor, ComprasEnc

class ProveedorForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    class Meta:
        model=Proveedor
        exclude = ['um','fm','uc','fc']
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

       #-------------------validacion para que no se repita el nombre del proveedor---------------- 
    def clean(self):
        try:
            sc = Proveedor.objects.get(
                descripcion=self.cleaned_data["descripcion"].upper() #preguntamos por un objeto, donde la descripcion, sea igual la que tenemos en la bd
            )

            if not self.instance.pk:  
                print("Registro ya existe")
                raise forms.ValidationError("Este registro ya existe")
            elif self.instance.pk!=sc.pk:                           #si se trata de editar uno que ya existe, por un valor que tambien ya existe
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio no permitido, ya existe un registro con esta descripcion")
        except Proveedor.DoesNotExist:
            pass
        return self.cleaned_data
       #-------------------validacion para que no se repita el nombre del proveedor----------------


class ComprasEncForm(forms.ModelForm):
    fecha_compra = forms.DateInput()
    fecha_factura = forms.DateInput()
    
    class Meta:
        model=ComprasEnc
        fields=['proveedor','fecha_compra','observacion',
            'no_factura','fecha_factura','sub_total',
            'descuento','total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['fecha_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True