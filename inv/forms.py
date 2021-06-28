from django import forms
from django.forms.widgets import NumberInput
from django.forms import ValidationError

from .models import Categoria, SubCategoria, Marca, Producto, Movimiento


class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields = ['descripcion','estado'] #campos que se van a cambiar
        labels = {'descripcion':"Descripción de la Categoría", #descripcion de la etiqueta
               "estado":"Estado"}
        widget={'descripcion': forms.TextInput} #tipo de elemento html

    def __init__(self, *args, **kwargs): 
        super().__init__(*args,**kwargs) 
        for field in iter(self.fields):  #recorrer todos los campos que se van a mostrar y que los itere
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
            

class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by('descripcion')
    )
    class Meta:
        model=SubCategoria
        fields = ['categoria','descripcion','estado']
        labels = {'descripcion':"Sub Categoría",
               "estado":"Estado"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['categoria'].empty_label =  "Seleccione Categoría"


class MarcaForm(forms.ModelForm):
    class Meta:
        model=Marca
        fields = ['descripcion','estado']
        labels= {'descripcion': "Descripción de la Marca",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

'''
class UMForm(forms.ModelForm):
    class Meta:
        model=UnidadMedida
        fields = ['descripcion','estado']
        labels= {'descripcion': "Descripción de la Marca",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
'''

class ProductoForm(forms.ModelForm):

    foto = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    codigo = forms.IntegerField(required=True,
        widget=NumberInput())

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if codigo < 0:
            raise ValidationError("Este campo no puede contener valores negativos")
        return codigo 

    codigo_barra = forms.IntegerField(required=True,
        widget=NumberInput())

    def clean_codigo_barra(self):
        codigo_barra = self.cleaned_data['codigo_barra']
        if codigo_barra < 0:
            raise ValidationError("Este campo no puede contener valores negativos")
        return codigo_barra 


    precio = forms.IntegerField(required=True,
        widget=NumberInput())

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise ValidationError("Este campo no puede contener valores negativos")
        return precio

    class Meta:
        model=Producto
        fields=[ 'nombre_producto', 'codigo','codigo_barra','descripcion','estado', \
                'precio','existencia','ultima_compra',
                'marca','subcategoria','foto']
        exclude = ['fm','uc','fc']
        widget={'nombre_producto': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True

       



class MovimientoForm(forms.ModelForm):

    fecha = forms.DateField(required=True,
    widget=NumberInput(attrs=({'type' : 'date'})))
    
    class Meta:
        model=Movimiento
        fields= ['producto', 'tipo_movimiento','fecha','cantidad', 'motivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ActualizacionPrecioForm(forms.ModelForm):

    choices_variacion = (
        ('costo', 'precio_costo'),
        ('venta', 'precio_venta')
    )

    choices_moneda = (
        ('pesos', '$'),
        ('porcentaje', '%')
    )


    subcategoria = forms.ModelChoiceField(queryset=SubCategoria.objects.all(),
                                   required=False,
                                   widget=forms.Select(attrs=(
                                       {
                                            'class': 'form-control'
                                       }
                                   )))                               

    variacion = forms.MultipleChoiceField(choices=choices_variacion,
                                          required=True,
                                          widget=forms.CheckboxSelectMultiple()
                                          )

    numero = forms.IntegerField(required=True,
                                widget=forms.NumberInput(attrs=(
                                    {
                                        'class': 'form-control'
                                    }
                                )))

    moneda = forms.MultipleChoiceField(choices=choices_moneda, required=True,
                                       widget=forms.CheckboxSelectMultiple(
                                           ))

    def clean_variacion(self):
        if len(self.cleaned_data['variacion']) >= 2:
            raise forms.ValidationError('Solo puede seleccionar 1 opción')
        return self.cleaned_data['variacion']

    def clean_moneda(self):
        if len(self.cleaned_data['moneda']) >= 2:
            raise forms.ValidationError('Solo puede seleccionar 1 opción')
        return self.cleaned_data['moneda']

    class Meta:
        fields = ['subcategoria', 'variacion', 'numero', 'moneda']
        model = Producto
