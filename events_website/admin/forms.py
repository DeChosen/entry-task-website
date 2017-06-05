from django import forms
from .models import user
from events.models import event, event_tags

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=254)
    class Meta:
        model = user
        fields = ['username', 'password']

    error_messages = {
        'invalid_login': ("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                checkUser = user.objects.filter(username = username)
            except:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': 'username'},
                )
            if checkUser and checkUser[0].password == password:
                return self.cleaned_data
            else:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': 'username'},
                )


class AddEventForm(forms.ModelForm):
    class Meta:
        model = event
	fields = ['name', 'location', 'date', 'description']

class AddTagForm(forms.ModelForm):
    class Meta:
        model = event_tags
        fields = ['tag']
        exclude = ('event_id',)
