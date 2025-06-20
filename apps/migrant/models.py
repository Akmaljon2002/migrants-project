from django.db import models
from django.utils.timezone import now

from apps.migrant.constants import GenderChoices
from django.utils.translation import gettext_lazy as _


class Migrant(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    region_id = models.IntegerField(verbose_name=_("Region ID"))
    district_id = models.IntegerField(verbose_name=_("District ID"))
    pinfl = models.CharField(
        max_length=14, unique=True, verbose_name=_("PINFL"),
    )
    birth_date = models.DateField(verbose_name=_("Birth Date"), blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        verbose_name=_("Gender"),
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )
    created_at = models.DateTimeField(default=now, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Migrant")
        verbose_name_plural = _("Migrants")
        db_table = 'migrant'
        ordering = ['-created_at']
