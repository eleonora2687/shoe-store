from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment'
        ]

        widgets = {
            'rating': forms.Select(
                choices=[
                    (1, '⭐'),
                    (2, '⭐⭐'),
                    (3, '⭐⭐⭐'),
                    (4, '⭐⭐⭐⭐'),
                    (5, '⭐⭐⭐⭐⭐'),
                ]
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            )
        }