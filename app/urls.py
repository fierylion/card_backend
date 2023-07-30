from django.urls import path
from .views import UserView, PaymentOperationView
app_urls = [
    path('user/register', UserView.as_view(
        {
            'post': 'create_single_user'
        }
    )),
    path('user/payment/generate', PaymentOperationView.as_view(
        {
            'post': 'create_payment_link'
        }
    )
    ),
    path('user/payment/callback', PaymentOperationView.as_view(
        {
            'post': 'receive_callback'
        }
    )),
]