from django import forms

from .models import Provincia, Localidad, Barrio
 

class ProvinciaForm(forms.ModelForm):
    class Meta:
        model=Provincia
        fields = ['nombre_provincia'] #campos que se van a cambiar
        labels = {'nombre_provincia':"Provincia"} #descripcion de la etiqueta
        widget={'nombre_provincia': forms.TextInput} #tipo de elemento html

    def __init__(self, *args, **kwargs): 
        super().__init__(*args,**kwargs) 
        for field in iter(self.fields):  #recorrer todos los campos que se van a mostrar y que los itere
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

    def clean(self):
        try:
            sc = Provincia.objects.get(
                nombre_provincia=self.cleaned_data["nombre_provincia"] #preguntamos por un objeto, donde la descripcion, sea igual la que tenemos en la bd
            )

            if not self.instance.pk:  
                print("Registro ya existe")
                raise forms.ValidationError("Este registro ya existe")
            elif self.instance.pk!=sc.pk:                           #si se trata de editar uno que ya existe, por un valor que tambien ya existe
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio no permitido, ya existe un registro con esta descripcion")
        except Provincia.DoesNotExist:
            pass
        return self.cleaned_data


class LocalidadForm(forms.ModelForm):
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all()
        .order_by('nombre_provincia')
    )
    class Meta:
        model=Localidad
        fields = ['provincia','nombre_localidad']
        labels = {'nombre_localidad':"Localidad"}
        widget={'nombre_localidad': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['provincia'].empty_label =  "Seleccione una Provincia"

    def clean(self):
        try:
            sc = Localidad.objects.get(
                nombre_localidad=self.cleaned_data["nombre_localidad"] #preguntamos por un objeto, donde la descripcion, sea igual la que tenemos en la bd
            )

            if not self.instance.pk:  
                print("Registro ya existe")
                raise forms.ValidationError("Este registro ya existe")
            elif self.instance.pk!=sc.pk:                           #si se trata de editar uno que ya existe, por un valor que tambien ya existe
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio no permitido, ya existe un registro con esta descripcion")
        except Provincia.DoesNotExist:
            pass
        return self.cleaned_data



class BarrioForm(forms.ModelForm):
    localidad = forms.ModelChoiceField(
        queryset=Localidad.objects.all()
        .order_by('nombre_localidad')
    )
    class Meta:
        model=Barrio
        fields = ['localidad','nombre_barrio']
        labels = {'nombre_barrio':"Barrio"}
        widget={'nombre_barrio': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['localidad'].empty_label =  "Seleccione una Localidad"


