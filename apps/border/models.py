from django.db import models


class BorderCross(models.Model):
    reg_date = models.DateField(verbose_name="Registration Date")
    endpoint_id = models.IntegerField(verbose_name="Endpoint ID")
    direction_type_code = models.CharField(
        max_length=10, verbose_name="Direction Type Code"
    )
    migrant_id = models.IntegerField(verbose_name="Migrant ID")
    trip_purpose_id = models.IntegerField(verbose_name="Trip Purpose ID")
    driection_country_id = models.IntegerField(
        verbose_name="Direction Country ID"
    )
    transport_type_code_id = models.IntegerField(
        verbose_name="Transport Type Code ID"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At"
    )

    class Meta:
        verbose_name = 'Border Cross'
        verbose_name_plural = 'Border Crosses'
        db_table = 'border_cross'
        ordering = ['-created_at']
