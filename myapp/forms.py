from django import forms
from .models import Review, Order


class ReviewForm(forms.ModelForm):
    """
        Валидация форм отзывов
    """

    MAX_SYMBOLS = 100

    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Максимум 100 символов'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')

        if len(text) > self.MAX_SYMBOLS:
            raise forms.ValidationError(f'Ваш отзыв не должен привышать {self.MAX_SYMBOLS} символов')

        return text

class OrderForm(forms.ModelForm):
    """
        Валидация форм заказов
    """

    class Meta:
        model = Order
        fields = ['name', 'phone', 'email', 'address', 'delivery_time', 'comment', 'payment_method']
        widgets = {
            'delivery_time': forms.TextInput(attrs={'placeholder': 'Пример: с 10 до 11.'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
            'payment_method': forms.Select()
        }
