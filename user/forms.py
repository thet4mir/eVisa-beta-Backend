from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm as DjangoAdminPasswordChangeForm

from main.forms import BaseModelForm


default_error_messages = {
    'required': 'оруулна уу!',
    'max_length': "%(limit_value)d-с илүүгүй урттай оруулна уу!",
    'min_length': "%(limit_value)d-с багагүй урттай оруулна уу!",
    'invalid': 'И-мэйл оруулна уу!',
    'unique': 'Энэ хэрэглэгч бүртгэгдсэн байна.',
}


class UserUpdateForm(forms.Form):
    email = forms.CharField(max_length=200)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    is_superuser = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].error_messages = default_error_messages


class PasswordValidationMixin():

    error_messages = {
        'password_incorrect': 'Нууц үг таарсангүй!',
        'password_mismatch': 'Нууц үг таарсангүй!',
        'password_too_similar': "Нууц үгийг нэвтрэх нэрээс ялгаатай оруулна уу!",
        'password_too_short': "%(min_length)d-с багаггүй урттай оруулна уу!",
        'password_too_common': "Нийтлэг нууц үг оруулсан байна!",
        'required': "оруулна уу!",
    }

    def add_error(self, field, error):
        if field == self.PASSWORD2_FIELD or field == 'old_password' or field == 'new_password1':
            errors = self.error_messages
            error = [
                forms.ValidationError(errors[e.code], code=e.code) if e.code in errors else e
                for e in error.error_list
            ]
            rval = super().add_error(field, error)
        else:
            rval = super().add_error(field, error)

        return rval


class AdminPasswordChangeForm(PasswordValidationMixin, DjangoAdminPasswordChangeForm):
    PASSWORD2_FIELD = 'password2'


class UserCreateForm(PasswordValidationMixin, UserCreationForm):

    PASSWORD2_FIELD = 'password2'

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].error_messages = default_error_messages

    def clean_password2(self):
        # Check that the two password entries match

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Нууц үг таарсангүй!")
        return password2


class UserToggleActiveForm(BaseModelForm):

    class Meta:
        model = get_user_model()
        fields = ('is_active',)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        if self.request.user.pk == self.instance.pk:
            self.add_error('is_active', "Өөрийгөө идэвхигүй болгох боломжгүй байна!")

        return super().clean()
