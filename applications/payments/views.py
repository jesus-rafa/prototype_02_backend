import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MercaodPagoSerializer


class mercadopago(APIView):

    #permission_classes = [IsAuthenticated]

    serializer_class = MercaodPagoSerializer

    def post(self, request, *args, **kwargs):
        serializer = MercaodPagoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        import mercadopago
        sdk = mercadopago.SDK("TEST-efd5f3a8-9688-472e-a087-3815220d2d58")

        # Crea un ítem en la preferencia
        preference_data = {
            "items": [
                {
                    "title": "Donacion",
                    "quantity": 1,
                    "unit_price": float(amount),
                }
            ],
            "back_urls":
                {
                    "success": "http://127.0.0.1:8000",
                    "failure": "http://127.0.0.1:8000",
                    "pending": "http://127.0.0.1:8000"
            },
            "auto_return": "approved"
        }
        # data = json.dumps({
        #     "items": [
        #         {
        #             "title": "Donacion",
        #             "quantity": 1,
        #             "unit_price": 10.5
        #         }
        #     ],
        #     "back_urls": {
        #         "success": "http://localhost:8080",
        #         "failure": "http://localhost:8080",
        #         "pending": "http://localhost:8080"
        #     },
        #     "auto_return": "approved"
        # })

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return Response({'response': preference})
