from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "username", "license_number"
        )

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != DriverLicenseUpdateForm.MAX_LENGTH:
            raise ValidationError(
                "License number must consist of 8 characters."
            )

        if not license_number[:3].isupper():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_number[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LENGTH = 8
    license_number = forms.CharField(
        required=True,
        validators=[MaxLengthValidator(MAX_LENGTH)],
    )

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
