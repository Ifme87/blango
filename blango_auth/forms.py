from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_registration.forms import RegistrationForm  # Django built-in retgistration

from blango_auth.models import User  # our custom User model


class BlangoRegistrationForm(RegistrationForm):  # Django built-in retgistration
    class Meta(RegistrationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(BlangoRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit("submit", "Register")
        )  # "submit" button named Register
