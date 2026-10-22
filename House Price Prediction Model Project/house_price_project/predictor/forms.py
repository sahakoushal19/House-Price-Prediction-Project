from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .locations import LOCATIONS, LOCATION_TYPES, all_city_choices, get_place


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PredictionForm(forms.Form):
    COUNTRY_CHOICES = [(country, country) for country in LOCATIONS]
    LOCATION_CHOICES = LOCATION_TYPES

    # Sensible limits keep the linear model inside a realistic range.
    area = forms.FloatField(min_value=100, max_value=50000)
    bedrooms = forms.IntegerField(min_value=1, max_value=15)
    bathrooms = forms.IntegerField(min_value=1, max_value=15)
    stories = forms.IntegerField(min_value=1, max_value=10)
    parking = forms.IntegerField(min_value=0, max_value=10)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    location_type = forms.ChoiceField(choices=LOCATION_CHOICES)
    # All city names are accepted here; clean() checks that the city really
    # belongs to the chosen country and location type. In the browser the
    # list is filtered by JavaScript as the user changes the other two boxes.
    city = forms.ChoiceField(choices=all_city_choices())

    def clean(self):
        cleaned = super().clean()
        country = cleaned.get("country")
        location_type = cleaned.get("location_type")
        city = cleaned.get("city")

        if country and location_type and city:
            if get_place(country, location_type, city) is None:
                self.add_error(
                    "city",
                    f"{city} is not listed as a {location_type} in {country}. "
                    "Please pick a city from the list.",
                )
        return cleaned
