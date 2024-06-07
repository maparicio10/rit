from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core.models import Officer


class OfficerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Officer
        fields = ('username', 'first_name', 'last_name', 'email')


class OfficerChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Officer
        fields = ('username', 'first_name', 'last_name', 'email')
