from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Address, Squadra, Azione


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignupForm(UserCreationForm):
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your shipping address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    billing_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your billing address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'shipping_address',
                                                 'billing_address')

    def save(self, commit=True):
        user = super().save(commit=commit)
        shipping_address = self.cleaned_data.get('shipping_address')
        billing_address = self.cleaned_data.get('billing_address')
        Address.objects.create(user=user, shipping_address=shipping_address, billing_address=billing_address)
        return user

class SquadraForm(forms.ModelForm):
    class Meta:
        model = Squadra
        fields = ['nome']

class AzioneForm(forms.Form):
    azioni = forms.ModelMultipleChoiceField(
        queryset=Azione.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )