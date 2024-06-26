from typing import Any
from django import forms
from .models import Dosen,Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm, SignupForm,ResetPasswordForm

# custom login and signUp form using allauth
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none'})
        self.fields['password'].widget.attrs.update({'class': 'bg-white text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none'})

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none'})
        self.fields['password1'].widget.attrs.update({'class': 'bg-white text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none'})
        self.fields['password2'].widget.attrs.update({'class': 'bg-white text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none'})

        self.fields['password1'].help_text = '<span class="text-sm text-gray-500">Your password can’t be too similar to your other personal information.</span>'
        self.fields['password2'].help_text = '<span class="text-sm text-gray-500">Enter the same password as before, for verification.</span>'

class CustomResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none',
            'placeholder': 'Email address',
        })
    )

class DosenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fakultas"].widget.attrs.update({
            "class":" border border-gray-300 text-black text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
        })
        self.fields["name"].widget.attrs.update({
            "class" :"bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none",
            'type' : "text",
        })
        self.fields["matakuliah"].widget.attrs.update({
            "class" :"bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none",
            'type' : "text",
        })

    class Meta:
        model = Dosen
        fields = ['name','fakultas','matakuliah']

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].widget.attrs.update({
            "class" :"h-32 w-full rounded border border-gray-300 bg-white py-1 px-3 text-base leading-6 text-gray-700 outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200",
            "style": "resize: none;",
        })
        self.fields["grade"].widget.attrs.update({
            "class":" border border-gray-300 text-black text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",

        })
        for field_name, field in self.fields.items():
            field.required = True

    class Meta:
        model = Review
        fields = ['rating','grade','body']

    rating = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect()
    )

# class signUpForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].widget.attrs.update({
#             "class" :"bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none",
#             'type' : "text",
#         })
#         self.fields["password1"].widget.attrs.update({
#             "class" :"bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none",
#             'type' : "password",
#         })
#         self.fields["password2"].widget.attrs.update({
#             "class" :"bg-white text-black focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block w-full appearance-none",
#             'type' : "password",
#         })

#         def clean_username(self):
#             username = self.cleaned_data.get('username').lower()

#             if User.objects.filter(username=username).exists():

#                 raise forms.ValidationError("Username already exists")
            
#             return username

#     class Meta:
#         model = User
#         fields = ['username','password1', 'password2']