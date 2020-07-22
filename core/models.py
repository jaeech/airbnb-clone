from django.db import models

# TimpeStampedModel을 기본으로 만들어서,
# 여러 Model에 같은방식으로 적용하기 위해 생성
class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Database에 저장되지 않게 하기 위해서
    class Meta:
        abstract = True
