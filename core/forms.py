from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core.models import Officer


class BaseOfficerForm(forms.ModelForm):
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("El nombre es obligatorio.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("El apellido es obligatorio.")
        return last_name


class OfficerCreationForm(UserCreationForm, BaseOfficerForm):
    class Meta(UserCreationForm.Meta):
        model = Officer
        fields = ("username", "first_name", "last_name", "email")


class OfficerChangeForm(UserChangeForm, BaseOfficerForm):
    class Meta(UserChangeForm.Meta):
        model = Officer
        fields = ("username", "first_name", "last_name", "email")
