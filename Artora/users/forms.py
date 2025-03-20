from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DesignerProfile

class ClientSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class DesignerSignUpForm(UserCreationForm):
    specialty = forms.ChoiceField(choices=DesignerProfile.Specialty.choices)
    experience = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    location = forms.CharField(max_length=255)
    experience_level = forms.ChoiceField(choices=DesignerProfile.ExperienceLevel.choices)
    pricing = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_designer = True  # Mark user as a designer
        if commit:
            user.save()
            DesignerProfile.objects.create(
                user=user,
                specialty=self.cleaned_data.get('specialty'),
                experience=self.cleaned_data.get('experience'),
                location=self.cleaned_data.get('location'),
                experience_level=self.cleaned_data.get('experience_level'),
                pricing=self.cleaned_data.get('pricing')
            )
        return user