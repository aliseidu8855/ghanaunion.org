from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('', views.membership_plans_view, name='plans'),
    path('initiate-payment/<int:tier_id>/', views.initiate_payment_view, name='initiate_payment'),
    path('payment-callback/', views.payment_callback_view, name='payment_callback'),
]