from django.contrib.auth import forms as admin_form
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_form.UserChangeForm):
    class Meta(admin_form.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_form.UserCreationForm):
    class Meta(admin_form.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }
