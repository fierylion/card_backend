from django.urls import path
from .views import UserView
app_urls = [
    path('user/register', UserView.as_view(
        {
            'post':'create_single_user'
        }
    ))
]