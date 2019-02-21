from django_redis import get_redis_connection
from django_redis.serializers.msgpack import MSGPackSerializer


class Carts:
    def __init__(self):
        self.redis = get_redis_connection("default")

    def get_cart_item(self, cart_id, product_id):
        msgpack_serializer = MSGPackSerializer(None)
        item = self.redis.hget('cart:{}'.format(cart_id), product_id)
        if item:
            item = msgpack_serializer.loads(item)

        return item

    def set_cart_item(self, cart_id, product_id, item_data):
        msgpack_serializer = MSGPackSerializer(None)
        self.redis.hmset('cart:{}'.format(cart_id), {product_id: msgpack_serializer.dumps(item_data)})

    def get_first_cart(self):
        carts = self.redis.keys('cart:*')
        if not carts:
            cart = None
        else:
            cart = carts[0].decode('utf-8').split(':')[1]

        return cart

    def get_carts_count(self):
        carts = self.redis.keys('cart:*')
        return len(carts)

    def get_cart_items(self, cart_id):
        msgpack_serializer = MSGPackSerializer(None)
        items = self.redis.hgetall('cart:{}'.format(cart_id))
        items = {key.decode('utf-8'): msgpack_serializer.loads(value) for key, value in items.items()}
        return items
