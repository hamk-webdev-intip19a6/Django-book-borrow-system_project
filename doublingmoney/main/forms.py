from django.contrib.auth.models import User
from django import forms
from .models import Rental, Book, Review

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label='comment')
    class Meta:
        model = Review
        fields = ['comment']

class RentForm(forms.ModelForm):
    D_CHOICES = [
        (2, '2 weeks'),
        (4, '4 weeks'),
        (6, '6 weeks')
    ]

    duration = forms.ChoiceField(choices=D_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Rental
        fields = []
        
    def clean_data(self):
        data = self.cleaned_data['duration']
        if (data):
            return data
        else:
            data = 2
            return data