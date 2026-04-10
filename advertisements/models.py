from django.db import models
from products.models import Product


class Advertisement(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Услуга",
    )
    budget = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Бюджет"
    )

    class Meta:
        verbose_name = "Рекламная компания"
        verbose_name_plural = "Рекламные компании"

    def __str__(self):
        return self.name