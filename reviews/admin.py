from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Review Admin Definition"""

    # __str__로 직접 네이밍을 불러올 수 있음
    list_display = ("__str__", "rating_average")
