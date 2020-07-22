from django.contrib import admin
from . import models

# Item이라는 항목으로 같이분류, 별도의 admin panel X
@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    pass

    # Admin에서 보여질 표시 방식

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths"),},),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        (
            "More About the Space",
            {
                # classes - collapse를 삽입함으로인해
                # 접었다 폈다 할 수 있는 항목으로 변함 (IE 안됨)
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        # 별도로 생성한 function
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    # Admin 패널이 자동으로 기본정렬이 됨 (작성 순서대로)
    # ordering = ("price", "bedrooms")

    # Admin에서 필터가능한 항목들
    list_filter = (
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # Admin 패널에 추가할 검색기능
    # search_fields 리트스 항목 앞에
    # ^를 붙이면, starts with ("^city")
    # =를 붙이면, exact ("=city")
    # @를 붙이면, search ("@city")
    # 아무것도 안붙이면, icontains
    # host 안에 있는 usernmae으로도 검색하고 싶다면
    # host__username을 추가
    search_fields = ["city", "host__username"]

    # 선택해서 선택항목으로 보내는 필터방식
    filter_horizontal = ("amenities", "facilities", "house_rules")

    # classname.object.* 등을 사용하여, QuerySet이용하여
    # 사용된 amenties의 개수를 확인
    def count_amenities(self, obj):
        return obj.amenities.count()

    # 매뉴얼 function에 대한 표시될 text 설정가능
    # count_amenities.short_description = "Hello"

    # classname.object.* 등을 사용하여, QuerySet이용하여
    # 저장된 photos 개수를 확인
    def count_photos(self, obj):
        return obj.photos.count()

