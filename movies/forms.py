from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
    
    review_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here...'}),
    )
