from django.db import models
from django.utils.translation import gettext_lazy as _


class ChartStatChoices(models.TextChoices):
    MIGRANTS_BY_COUNTRY = "migrants_by_country", _("Migrants by Country")
    MIGRANTS_BY_REGION = "migrants_by_region", _("Migrants by Region")
    MIGRATION_PURPOSE = "migration_purpose", _("Migration Purpose")
    TRANSPORT_TYPE = "transport_type", _("Transport Type")