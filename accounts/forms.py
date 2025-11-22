from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile


User = get_user_model()


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Work email")

    def clean_email(self) -> str:
        email = self.cleaned_data["email"].strip().lower()
        if not email.endswith("@murweh.qld.gov.au"):
            raise forms.ValidationError(
                "Only @murweh.qld.gov.au email addresses are allowed."
            )
        return email


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = UserProfile
        fields = ["job_title", "department", "phone_number", "location"]

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name

    def save(self, commit: bool = True) -> UserProfile:  # type: ignore[override]
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        if commit:
            self.user.save()
            profile.user = self.user
            profile.require_profile_update = False
            profile.save()
        return profile


