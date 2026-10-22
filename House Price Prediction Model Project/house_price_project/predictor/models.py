from django.db import models
from django.contrib.auth.models import User

from .locations import CURRENCY_SYMBOLS
from .pricing import group_indian


class Prediction(models.Model):
    """One saved prediction, tied to the customer who made it."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="predictions",
    )

    # Inputs
    area = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    stories = models.IntegerField()
    parking = models.IntegerField()
    country = models.CharField(max_length=20)
    location_type = models.CharField(max_length=20)
    city = models.CharField(max_length=60, blank=True, default="")

    # Outputs
    base_price = models.FloatField(help_text="Raw ML model output, before location adjustment")
    location_multiplier = models.FloatField(
        help_text="City market level x fame factor applied to the base price"
    )
    predicted_price = models.FloatField(help_text="Final price shown to the user")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def currency_symbol(self):
        return CURRENCY_SYMBOLS.get(self.country, "")

    @property
    def price_display(self):
        """Price in lakh/crore digit grouping, e.g. 2,84,00,000."""
        return group_indian(self.predicted_price)

    def __str__(self):
        place = self.city or self.location_type
        return f"{self.user.username} | {place}, {self.country} | {self.predicted_price}"
