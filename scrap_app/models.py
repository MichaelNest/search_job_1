import jsonfield
from django.db import models
from scrap_app.utils import from_cyrillic_to_latinic


def default_urls():
    return {'work': '', 'rabota': '', 'dou': '', 'djinni': ''}


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
        
class Vacantion(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=222, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=222, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    datestamp = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-datestamp']
        
    def __str__(self):
        return self.title

class Error(models.Model):
    datestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)
    
    class Meta:
        unique_together = ('city', 'language')