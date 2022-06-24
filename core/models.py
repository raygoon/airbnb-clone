from django.db import models


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    # auto_now_add = True 는 장고가 모델을 생성하면 현재날짜와 시간을 여기에 넣어준다는 뜻이다.
    # auto_now = True 는 내가 모델을 저장할때 마다 항상 새로운 날짜를 업데이트 해준다는 뜻이다.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # abstract 추상모델은 모델이지만 데이터베이스에는 나타나지 않는 모델을 말한다.
    # 대부분의 추상모델은 확장을 위해 사용된다.
    # 이걸 설정하지 않으면 데이터베이스에 이 모델이 등록된다.

    class Meta:
        abstract = True
