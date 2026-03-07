import re

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


    def clean_name(self):
        name=self.cleaned_data.get('name')
        if len(name) < 2 or len(name) > 25:
            raise forms.ValidationError('Имя должно содержать не менее 2-х и не более 15 символов.')
        return name

    def clean_phone(self):
        phone=self.cleaned_data.get('phone')
        if not re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone):
            raise forms.ValidationError('Введите корректный номер телефона. Пример: +79005001020')
        return phone

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError('Введите корректную почту. Пример: user@example.com')
        return email