from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ArtistList

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label = "Name")
    last_name = forms.CharField(label = "Surname")
 
    # this sets the order of the fields
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2", )
 
    # this redefines the save function to include the fields you added
    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        lis = ArtistList(list_name="faves", user= user)
        lis.save()      
        return user