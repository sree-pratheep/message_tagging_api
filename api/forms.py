from django import forms


class MessageTagForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    category = forms.ChoiceField(choices=[('india','India'), ('tamilnadu', 'Tamil Nadu')])
    type = forms.ChoiceField(choices=[('stats','Stats'), ('news','News')])
    media_path = forms.CharField(widget=forms.HiddenInput())
