from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class BorderCross(models.Model):
    reg_date = models.DateField(verbose_name=_("Registration Date"))
    endpoint_id = models.IntegerField(verbose_name=_("Endpoint ID"))
    direction_type_code = models.CharField(
        max_length=10, verbose_name=_("Direction Type Code")
    )
    migrant_id = models.IntegerField(verbose_name=_("Migrant ID"))
    trip_purpose_id = models.IntegerField(verbose_name=_("Trip Purpose ID"))
    driection_country_id = models.IntegerField(
        verbose_name=_("Direction Country ID")
    )
    transport_type_code_id = models.IntegerField(
        verbose_name=_("Transport Type Code ID")
    )

    created_at = models.DateTimeField(default=now, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Border Cross")
        verbose_name_plural = _("Border Crosses")
        db_table = 'border_cross'
        ordering = ['-created_at']
