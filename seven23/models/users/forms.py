from django import forms
from django.contrib.auth.models import User

# Create a django form to create a superuser
class SuperUserForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        # If there is one or more user existing we raise an error
        if User.objects.count() > 0:
            raise forms.ValidationError('There is already a superuser')

        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_superuser(username, email, password)
        return user