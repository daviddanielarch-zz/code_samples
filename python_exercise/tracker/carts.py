import uuid

from django_redis import get_redis_connection

CART_KEYSPACE = 'cart'
ITEM_KEYSPACE = 'item'


class Carts:
    def __init__(self):
        self.redis = get_redis_connection("default")

    def get_cart_item(self, cart_id, product_id):
        item = None

        item_uuid = self.redis.hget('{}:{}'.format(CART_KEYSPACE, cart_id), product_id)
        if item_uuid:
            item = self.redis.hgetall('{}:{}'.format(ITEM_KEYSPACE, item_uuid.decode('utf-8')))
            item = {key.decode('utf-8'): value.decode('utf-8') for key, value in item.items()}
            item['price'] = int(item['price']) if item['price'] else ''
        return item

    def set_cart_item(self, cart_id, product_id, item_data):
        item_uuid = self.redis.hget('{}:{}'.format(CART_KEYSPACE, cart_id), product_id)
        if not item_uuid:
            item_uuid = str(uuid.uuid4())
            self.redis.hmset('{}:{}'.format(CART_KEYSPACE, cart_id), {product_id: item_uuid})
        else:
            item_uuid = item_uuid.decode('utf-8')

        self.redis.hmset('{}:{}'.format(ITEM_KEYSPACE, item_uuid), item_data)

    def get_first_cart(self):
        carts = self.redis.keys('{}:*'.format(CART_KEYSPACE))
        if not carts:
            cart = None
        else:
            cart = carts[0].decode('utf-8').split(':')[1]

        return cart

    def get_carts_count(self):
        carts = self.redis.keys('{}:*'.format(CART_KEYSPACE))
        return len(carts)

    def get_cart_items(self, cart_id):
        items = self.redis.hgetall('{}:{}'.format(CART_KEYSPACE, cart_id))
        item_uuids = [(product_id, product_uuid) for product_id, product_uuid in items.items()]
        items = {product_id: self.redis.hgetall('{}:{}'.format(ITEM_KEYSPACE, product_uuid)).items() for product_id, product_uuid in item_uuids}
        return items
