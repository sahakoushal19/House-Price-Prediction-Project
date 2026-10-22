from django.contrib import admin

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "country",
        "location_type",
        "city",
        "area",
        "base_price",
        "location_multiplier",
        "predicted_price",
        "created_at",
    )
    list_filter = ("country", "location_type", "city")
    search_fields = ("user__username", "city")
