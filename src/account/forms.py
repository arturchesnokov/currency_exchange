from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.shortcuts import get_object_or_404

from account.models import User, ActivationCodeSms


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'phone')

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords not equal!')
        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()

        sms_codes = user.sms_codes.create()
        sms_codes.send_activation_code()

        return user


class ActivateForm(forms.Form):
    sms_code = forms.CharField()
    # user_id = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            code = cleaned_data['sms_code']
            user_id = cleaned_data['user_id']
            ac = get_object_or_404(
                ActivationCodeSms.objects.select_related('user'),
                code=code,
                user_id=user_id,
                is_activated=False
            )

            if cleaned_data['password'] != cleaned_data['password2']:
                raise forms.ValidationError('Passwords not equal!')
        return cleaned_data

    def save(self, commit=True):
        ac = get_object_or_404(
            ActivationCodeSms.objects.select_related('user'),
            code=code,
            user_id=user_id,
            is_activated=False
        )



    if ac.is_expired:
        raise Http404

    ac.is_activated = True
    ac.save(update_fields=['is_activated'])

    user = ac.user
    user.is_active = True
    user.save(update_fields=['is_active'])
