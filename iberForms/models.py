from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

typeChoice = (
    ("sales", "Sales"),
    ("retention", "Retention")
)


class CECDisplay(models.Model):
    entry_date = models.DateTimeField(auto_now_add=True)
    entry_type = models.CharField(
        max_length=50, blank=False, choices=typeChoice)
    current = models.IntegerField(
        validators=[MinValueValidator(0)], blank=False)
    target = models.IntegerField(
        validators=[MinValueValidator(0)], blank=False)
