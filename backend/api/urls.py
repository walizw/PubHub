# custom urls
from django.urls import path

from . import views

urlpatterns = [
    path(".well-known/webfinger",
         views.WellKnownAPIView.as_view(), name="well-known"),

    path("api/v1/users/<str:username>", views.UserAPIView.as_view(), name="user"),
    path("api/v1/users/<str:username>/inbox",
         views.InboxAPIView.as_view(), name="inbox"),
    path("api/v1/users/<str:username>/outbox",
         views.OutboxAPIView.as_view(), name="outbox"),
    path("api/v1/users/<str:username>/followers",
         views.FollowersAPIView.as_view(), name="followers"),
    path("api/v1/users/<str:username>/following",
         views.FollowingAPIView.as_view(), name="following"),
]
