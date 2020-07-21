from django.db import models


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
