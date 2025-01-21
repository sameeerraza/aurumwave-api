from django.urls import path

from product.views import RequestListCreateView, RequestRetrieveUpdateDestroyView

urlpatterns = [
    path('products', RequestListCreateView.as_view()),
    path('products/<int:request_id>', RequestRetrieveUpdateDestroyView.as_view()),
]
