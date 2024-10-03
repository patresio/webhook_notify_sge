from django.urls import path

from webhooks.views import WebhookOrderView

urlpatterns = [
    path("order/", WebhookOrderView.as_view(), name="webhook-order"),
]
