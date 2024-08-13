from django import forms
from .models import Mangas

class MangaForm(forms.ModelForm):
    class Meta:
        model = Mangas
        fields = '__all__'
