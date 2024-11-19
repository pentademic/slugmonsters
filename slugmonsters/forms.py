from django import forms
 
from .models import Slug
 
class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Slug
        fields = ('lieu',)