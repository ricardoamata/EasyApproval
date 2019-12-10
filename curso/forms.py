from django import forms
from .models import Curso


class CursoForm(forms.ModelForm):
    fecha_inicial = forms.DateField(
        widget = forms.DateInput(format='%d/%m/%Y', attrs={'class': 'uk-input'}),
        input_formats = ('%d/%m/%Y', )
    )

    fecha_final = forms.DateField(
        widget = forms.DateInput(format='%d/%m/%Y', attrs={'class': 'uk-input'}),
        input_formats = ('%d/%m/%Y', )
    )

    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicial'].required = False
        self.fields['fecha_final'].required = False
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = (
                'uk-select' if key == 'instructor' 
                else 'uk-textarea' if key == 'descripcion' 
                else 'uk-textarea' if key == 'obj_general' 
                else 'uk-textarea' if key == 'obj_particular'
                else 'uk-textarea' if key == 'contenido_sintetico' 
                else 'uk-textarea' if key == 'estilo_enseñanza' 
                else 'uk-textarea' if key == 'req_evaluacion'
                else 'uk-textarea' if key == 'bibliografia' 
                else 'uk-textarea' if key == 'experiencia' 
                else 'uk-textarea' if key == 'hab_alumnos'
                
                else 'uk-input'
            )

    class Meta:
        model = Curso
        fields = '__all__'
        exclude = ['slug', 'estado', 'alumnos', 'hash_id']