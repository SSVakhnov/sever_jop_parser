from django.db import models

from apps.scraper.cosntants.enums import CategoryType, PositionType


class BaseModel(models.Model):
    """ Опиисывает панраметры стандартной модели """

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        abstract = True


class GeoModel(models.Model):
    """ Описывает гео позицию """
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        abstract = True


class BaseVacancy(models.Model):
    """ Модель описывает базовые атрибуты вакансии """
    category = models.CharField(choices=CategoryType.choices(), max_length=255, null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    position = models.CharField(choices=PositionType.choices(), max_length=255, null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        abstract = True


class SearchParam(BaseModel, BaseVacancy, GeoModel):
    """ Хранит параметры поиска для данных к парсингу """

    search_text = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        ordering = ['id']


class Vacancy(BaseModel, BaseVacancy, GeoModel):
    """ Описывает результат парсинга ресурса """
    header = models.CharField(max_length=255, null=True, blank=True)
    short_description = models.CharField(max_length=512, null=True, blank=True)
    full_description = models.CharField(max_length=512, null=True, blank=True)
    requirements = models.CharField(max_length=512, null=True, blank=True)
    responsibility = models.CharField(max_length=512, null=True, blank=True)
    bonuses = models.CharField(max_length=512, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.header} | {self.company_name}'
