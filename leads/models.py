from django.db import models
from advertisements.models import Advertisement


class Lead(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
        verbose_name="Рекламная компания",
    )

    class Meta:
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"