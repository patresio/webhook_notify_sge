from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class WebhookOrderView(APIView):

    def post(self, request):
        data = request.data

        print(data)

        return Response(data=data, status=status.HTTP_200_OK)
