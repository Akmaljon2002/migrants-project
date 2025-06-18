from django.db import models


class Migrant(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    region_id = models.IntegerField(verbose_name="Region ID")
    district_id = models.IntegerField(verbose_name="District ID")
    pinfl = models.CharField(
        max_length=14, unique=True, verbose_name="PINFL"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = 'Migrant'
        verbose_name_plural = 'Migrants'
        db_table = 'migrant'
        ordering = ['-created_at']
