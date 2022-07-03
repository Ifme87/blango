from django import forms
from blog.models import Comment
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper

#1) create model Comment 2) create class form 3) insert class form into view 4) route to view
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))