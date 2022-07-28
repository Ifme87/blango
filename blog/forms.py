from django import forms
from .models import Tag
from blog.models import Comment, Post
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from .widgets import RelatedFieldWidgetCanAdd

#1) create model Comment 2) create class form 3) insert class form into view 4) route to view
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class CreateThreadForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Tag.objects.all(),
        widget=RelatedFieldWidgetCanAdd(Tag, related_url="blog:so_tag_add"),
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1}),
            'content': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateThreadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['value']
        widgets = {
            'value': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateTagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
