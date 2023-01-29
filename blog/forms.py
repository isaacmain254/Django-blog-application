from django import forms
from .models import Comment

# form for sharing posts using email
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

# form for creating comments from models
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

# search form
class SearchForm(forms.Form):
    query = forms.CharField()