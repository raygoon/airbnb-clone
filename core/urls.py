from django.urls import path
from rooms import views as room_views

app_name = "core"

urlpatterns = [
    # "" 은 / 를 의미한다.
    path("", room_views.HomeView.as_view(), name="home")
]
