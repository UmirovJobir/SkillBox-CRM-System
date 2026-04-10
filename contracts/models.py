from django.db import models
from products.models import Product
from customers.models import Customer


class Contract(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Услуга",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contracts",
        verbose_name="Клиент",
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Стоимость"
    )

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"

    def __str__(self):
        return self.name