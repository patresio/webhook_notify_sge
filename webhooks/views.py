import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from services.callmebot import CallMeBot
from webhooks.messages import outflow_message
from webhooks.models import Webhook


class WebhookOrderView(APIView):

    def post(self, request):
        data = request.data
        Webhook.objects.create(
            event_type=data.get("event_type"),
            system=data.get("system"),
            event=json.dumps(data, ensure_ascii=False),
        )

        message = outflow_message.format(
            data.get("system"),
            data.get("product"),
            data.get("quantity"),
            data.get("product_selling_price") * data.get("quantity"),
            (data.get("product_selling_price") - data.get("product_cost_price"))
            * data.get("quantity"),
        )

        callmebot = CallMeBot()
        callmebot.send_message(message)

        # send_mail(
        #     subject="Nova saída registrada no {}!".format(data.get("system")),
        #     message="",
        #     from_email=f'{data.get("system")} <{settings.EMAIL_HOST_USER}>',
        #     recipient_list=[settings.EMAIL_ADMIN_RECEIVER],
        #     fail_silently=False,
        #     html_message=render_to_string(
        #         "outflow.html",
        #         {
        #             "system": data.get("system"),
        #             "product": data.get("product"),
        #             "quantity": data.get("quantity"),
        #             "total_value": data.get("product_selling_price")
        #             * data.get("quantity"),
        #             "profit_value": (
        #                 data.get("product_selling_price")
        #                 - data.get("product_cost_price")
        #             )
        #             * data.get("quantity"),
        #         },
        #     ),
        # )

        return Response(data=data, status=status.HTTP_200_OK)
