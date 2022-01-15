from django.urls import path

from apps.scraper.views import (
    index_view, debug_view
)

urlpatterns = [
    path('', index_view),
    path('debug/', debug_view),
]
