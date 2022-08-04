from django.db import models
from django.conf import settings

# Create your models here.


class QuestionsForm(
    models.Model
):  # what's the difference between 'forms.Form', 'forms.ModelForm', 'models.Model'?
    color = models.CharField(max_length=200)
    car = models.CharField(max_length=200)
    beer = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="email"
    )
