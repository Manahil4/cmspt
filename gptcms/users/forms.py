from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Discussion, Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_picture', 'bio', 'social_links', 'is_client', 'is_designer')

class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_picture', 'bio', 'social_links')

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        # Include all relevant fields for the Discussion model
        fields = ('topic', 'description')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Include all relevant fields for the Comment model
        fields = ('content', 'discussion')
