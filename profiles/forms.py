from django import forms

from .models import Profile

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        )
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "type": "email", "placeholder": "Email"})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write a few words about yourself...",
            }
        )
    )
    photo = forms.ImageField(
        label="Profile Photo",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control"
            }
        )
    
    )

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email", "bio", "photo"]

    # The following is to prepopulated the data as placeholder.
    # def __init__(self, *args, **kwargs):
    #     super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
    #     instance = kwargs.get('instance')
    #     if instance:
    #         self.fields['first_name'].widget.attrs.update({'placeholder': instance.first_name, 'class': 'form-control'})
    #         self.fields['last_name'].widget.attrs.update({'placeholder': instance.last_name, 'class': 'form-control'})
    #         self.fields['email'].widget.attrs.update({'placeholder': instance.email, 'class': 'form-control'})
    #         self.fields['bio'].widget.attrs.update({'placeholder': instance.bio, 'class': 'form-control'})
