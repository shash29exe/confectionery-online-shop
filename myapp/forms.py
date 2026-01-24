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


class OrderForm(forms.ModelForm):
    """
        Валидация форм заказов
    """

    class Meta:
        model = Order
        fields = ['name', 'phone', 'email', 'address', 'delivery_time', 'comment']
        widgets = {
            'delivery_time': forms.TextInput(attrs={'placeholder': 'Пример: с 10 до 11.'}),
            'comment': forms.Textarea(attrs={'rows': 3})
        }
