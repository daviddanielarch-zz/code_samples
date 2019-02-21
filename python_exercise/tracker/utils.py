from rest_framework import serializers
from rest_framework.exceptions import ValidationError


# Taken from https://docs.python.org/3/library/itertools.html
def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    result = next(filter(pred, iterable), default)
    if result:
        return result
    else:
        return None


def validate_uuid(value):
    try:
        cart_id = serializers.UUIDField().to_internal_value(data=value)
    except ValidationError:
        cart_id = None

    return cart_id

