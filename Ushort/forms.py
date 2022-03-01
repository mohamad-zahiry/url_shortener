from django.forms import EmailField, Form, CharField, PasswordInput, EmailInput
from django.utils.translation import gettext_lazy as _
from Ushort.models import Creator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CreatorSignUpForm(Form):
    email = EmailField(widget=EmailInput(attrs={"class": "form-control-input", "id": "semail"}))
    password = CharField(widget=PasswordInput(attrs={"class": "form-control-input", "id": "spassword"}))

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if Creator.objects.filter(email=email).exists():
            raise ValidationError(_("This email has been used before"))
        return email

    def save(self, *args, **kwargs):
        email, password = self.cleaned_data.values()
        user = User.objects.create_user(username=email, password=password)
        Creator.objects.create(user=user, email=email)


class CreatorLogInForm(Form):
    email = EmailField(widget=EmailInput(attrs={"class": "form-control-input", "id": "lemail"}))
    password = CharField(widget=PasswordInput(attrs={"class": "form-control-input", "id": "lpassword"}))

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        creator = Creator.objects.filter(email=email)
        if not creator.exists():
            raise ValidationError(_("This email has not been registered before"))
        return email
