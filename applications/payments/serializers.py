from rest_framework import serializers


class MercaodPagoSerializer(serializers.Serializer):
    """ serializador para donacion con mercadopago """

    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
