from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from .models import Subscription


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'subscription/captcha.html'


class SubscriptionForm(forms.ModelForm):
    """Форма подписки по Email"""

    captcha = CaptchaField(widget=CustomCaptchaTextInput(
        attrs={'class': 'input-captcha form-control',
               'placeholder': 'Введите капчу'}))

    class Meta:
        model = Subscription
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ваш E-mail'})
        }
        labels = {
            'email': ''
        }
