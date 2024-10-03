import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from webhooks.models import Webhook


class WebhookOrderView(APIView):

    def post(self, request):
        data = request.data
        Webhook.objects.create(
            event_type=data.get("event_type"),
            event=json.dumps(data, ensure_ascii=False),
        )
        return Response(data=data, status=status.HTTP_200_OK)
