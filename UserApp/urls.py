from django.urls import path
from .views import UserSignupView, SearchCommonUsersView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('search/', SearchCommonUsersView.as_view(), name='search-users'),
]
