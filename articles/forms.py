from django import forms
from .models import Comment, Articles


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
    
class CommentForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #       super().__init__(*args, **kwargs)
    #       self.fields["text"].required = False
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
    
        
class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'content', 'categories', 'image', 'tags', 'status']
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         self.fields['author'].initial = self.instance.author.username
    #     else:
    #         self.fields['author'].initial = kwargs.get('author', '')
    #         if not self.fields['author'].initial:
    #             self.fields['author'].initial = request.user.username

    #     # Update this line
    #     self.fields['author'].initial = self.fields['author'].initial or request.user.username
        
class SearchBook(forms.Form):
    text = forms.CharField(max_length=100)