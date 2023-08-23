
from django import forms 
from .models import District

class ShortestDistanceForm(forms.Form):
    source_district = forms.ModelChoiceField(queryset=District.objects.all(), widget=forms.Select(attrs={'class': 'form-select col-6'}))
    destination_district = forms.ModelChoiceField(queryset=District.objects.all(), widget=forms.Select(attrs={'class': 'form-select col-6'}))
    
    def clean(self):
        cleaned_data = super().clean()
        source_district = cleaned_data.get('source_district')
        destination_district = cleaned_data.get('destination_district')
        
        if source_district == destination_district:
            print('asdfasd')
            raise forms.ValidationError("Source and destination districts cannot be the same.")
        return self.cleaned_data