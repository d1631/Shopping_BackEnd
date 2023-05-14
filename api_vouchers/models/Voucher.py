from django.db import models
from api_base.models import TimeStampedModel


class Voucher(TimeStampedModel):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'voucher'
        ordering = ['-created_at', ]

    def __str__(self):
        return str(self.id)
