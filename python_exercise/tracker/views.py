import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response

from tracker.carts import Carts
from tracker.serializers import ItemEndpointSerializer
from tracker.utils import first_true, validate_uuid


@api_view(['POST'])
def items(request):
    """
    I'm not putting a docstring with the endpoint information as it would imply copying
    pretty much all that the Endpoint specification already tells
    We can use that as the API doc
    """
    carts = Carts()
    serializer = ItemEndpointSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    product_id = serializer.validated_data.get('product_id')
    cart_id = get_or_generate_cart_id(request)

    item_data = carts.get_cart_item(cart_id, product_id)
    if item_data:
        # Don't overwrite existing data if name or price is not in args
        name = serializer.validated_data.get('name', item_data['name'])
        price = serializer.validated_data.get('price', item_data['price'])
    else:
        name = ''
        price = ''

    item = {
        'name': name,
        'price': price
    }

    carts.set_cart_item(cart_id, product_id, item)

    response = Response({'cart_id': cart_id})
    response.set_cookie('cart_id', cart_id)

    return response


def get_or_generate_cart_id(request):
    cart_id = first_true([validate_uuid(request.COOKIES.get('cart_id')), validate_uuid(request.data.get('cart_id'))])
    if not cart_id:
        cart_id = str(uuid.uuid4())

    return cart_id
