from django.db import models
from django.utils import timezone
from datetime import timedelta

class Medicine(models.Model):
    """
    Represents a medicine in the inventory.
    """
    # (Choices fields remain the same...)
    ADMINISTRATION_TYPE_CHOICES = [
        ('oral', 'Oral'),
        ('inj', 'Injection'),
        ('topical', 'Topical'),
        ('inhal', 'Inhalation'),
    ]

    COUNT_TYPE_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('ampoule', 'Ampoule'),
        ('vial', 'Vial'),
        ('bottle', 'Bottle'),
        ('tube', 'Tube'),
    ]

    name = models.CharField(
        max_length=200,
        help_text="The brand or generic name of the medicine."
    )
    composition = models.CharField(
        max_length=255,
        help_text="The active ingredients and their strength (e.g., 'Paracetamol 500mg')."
    )
    administration_type = models.CharField(
        max_length=10,
        choices=ADMINISTRATION_TYPE_CHOICES,
        default='oral',
        help_text="How the medicine is administered."
    )
    category = models.CharField(
        max_length=100,
        help_text="The therapeutic category (e.g., 'Analgesic', 'Antibiotic')."
    )
    count_type = models.CharField(
        max_length=20,
        choices=COUNT_TYPE_CHOICES,
        default='tablet',
        help_text="The unit of the medicine (e.g., tablet, bottle)."
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="The total quantity currently in stock."
    )
    expiration_date = models.DateField(
        help_text="The expiration date of the medicine batch."
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional notes or remarks."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'composition']
        verbose_name = "Medicine"
        verbose_name_plural = "Medicines"

    def __str__(self):
        return f"{self.name} ({self.composition})"

    @property
    def is_expired(self):
        """Returns True if the medicine's expiration date is in the past."""
        return self.expiration_date < timezone.now().date()
    
    @property
    def is_near_expiry(self):
        """
        Returns True if the medicine is not expired and will expire within the next 90 days.
        """
        if self.is_expired:
            return False
        today = timezone.now().date()
        ninety_days_from_now = today + timedelta(days=90)
        return self.expiration_date <= ninety_days_from_now

