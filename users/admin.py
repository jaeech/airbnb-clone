from django.contrib import admin

# 이것저것 설정되어있는 UserAdmin을 불러오기
from django.contrib.auth.admin import UserAdmin

# 같은 폴더 내에서 models를 import 해와라
from . import models

# 이렇게 UsersApp을 추가하거나
# models.User = 만든 userApp
# CustomerUSerAdmin admin 패널에서 컨트롤 할 수 있는 user class
# admin.site.register(models.User, CustomUserAdmin)

# 밑에처럼 추가할 수 있음
# @admin.register(models.User)
# class CustomUserAdmin(UserAdmin):  <---- 경우 잘 설정되어있는 UserAdmin 불러오는거
# class CustomUserAdmin(admin.ModelAdmin): <---- 의 경우 기본 Admin을 불러오는거
#    pass
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    pass

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

