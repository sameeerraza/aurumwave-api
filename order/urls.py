from django.urls import path

from order.views import OrderCreateView

urlpatterns = [
    path("orders", OrderCreateView.as_view(), name="bulk-order-create"),
]
