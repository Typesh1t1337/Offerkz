from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm


class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['photo']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'type': 'file',
                                            'accept': 'image/*',
                                            'id':'photo-input',
                                            'onchange': 'previewImage(event)',
                                            'name':'photo'
                                                     })
        }




class updatePasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput,
        error_messages={'required':'Поле пароля является обязательным'})
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput,
        error_messages={'required':'Поле пароля является обязательным'})
    new_password2 = forms.CharField(
        label="Повторите пароль"
        ,widget=forms.PasswordInput,
        error_messages={'required':'Поле пароля является обязательным'})


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = get_user_model()

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            self.add_error('Введенный пароль не совпадает с вашим')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('Пароли не совпадают')
        if new_password1 and new_password2 and str(new_password1).isdigit() and str(new_password2).isdigit():
            self.add_error('Пароль слишком легкий, пароль должен состоять из цифер и букв')
        if new_password1 and new_password2 and str(new_password1).isalpha() and str(new_password2).isalpha():
            self.add_error('Пароль слишком легкий, пароль должен состоять из цифер и букв')
        return cleaned_data



