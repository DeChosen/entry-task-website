from django import forms
from .models import Photo, event_comments

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        exclude = ('event_id',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = event_comments
        fields = ['comment']
        exclude = ('commenter_name', 'date','event_id',)

