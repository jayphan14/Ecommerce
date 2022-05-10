
from django.forms import ModelForm
from django import forms




class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    bid = forms.CharField(widget=forms.NumberInput(attrs={'step':'0.01', 'min':'0'}))
    url = forms.CharField(widget=forms.URLInput())
    category = forms.CharField(label="Category")
    

class BidForm(forms.Form):
    bidValue = forms.CharField(widget=forms.NumberInput(attrs={'step':'0.01', 'min':'0'}))