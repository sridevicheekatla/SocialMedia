"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from socialmedia_app.views import (
    SignupView,
    SearchUsersView,
    SendFriendRequestView,
    HandleFriendRequestView,
    ListFriendsView,
    ListPendingRequestsView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # jwt
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # social media
    path('signup/', SignupView.as_view(), name='signup'),
    path('search-users/', SearchUsersView.as_view(), name='search-users'),
    path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('handle-friend-request/', HandleFriendRequestView.as_view(), name='handle-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='friends'),
    path('pending-requests/', ListPendingRequestsView.as_view(), name='pending-requests'),
]
