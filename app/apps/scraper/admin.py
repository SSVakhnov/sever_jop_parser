from django.contrib import admin

from apps.scraper.models import (
    Vacancy, SearchParam
)

admin.site.register(SearchParam)
admin.site.register(Vacancy)
