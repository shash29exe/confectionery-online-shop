from django import forms
from .models import Review, Order

class ReviewForm(forms.ModelForm):
    """
        Валидация форм отзывов
    """

    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш отзыв'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }