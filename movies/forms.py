from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here...'}),
        }