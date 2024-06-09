from django.forms import ModelForm, TimeInput, TextInput, Textarea
from .models import Reviews


class ReviewsForms(ModelForm):
    class Meta:
        model = Reviews
        fields = ['name', 'description']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание',
                'maxlength': '30',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Полный текст отзыва',
            })

        }
