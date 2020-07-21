from django.db import models
from scrap_app.utils import from_cyrillic_to_latinic


class City(models.Model):
    name = models.CharField(max_length=55,
                            verbose_name='Название города',
                            unique=True)
    slug = models.SlugField(max_length=55, blank=True)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_latinic(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=55,
                            verbose_name='Язык программирования',
                            unique=True)
    slug = models.SlugField(max_length=55, blank=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_latinic(str(self.name))
        super().save(*args, **kwargs)
