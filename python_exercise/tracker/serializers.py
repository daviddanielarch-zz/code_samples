from rest_framework import serializers


class ItemEndpointSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    price = serializers.IntegerField(required=False, allow_null=True)
