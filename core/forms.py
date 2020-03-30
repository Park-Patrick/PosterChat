from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class AdminAddUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  "username", "avatar", "description",)

    def clean_password2(self):
        """Checks that the two passwords match
        """

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do no match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class AdminUpdateUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "email", "password", "first_name", "last_name", "username", "is_active", "is_staff", "avatar", "description",
        )

    def clean_password(self):
        return self.initial["password"]


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name",
                  "username", "avatar", "description")
