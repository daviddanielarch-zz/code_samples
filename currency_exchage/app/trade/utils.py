from decimal import Decimal, ROUND_DOWN

UID_MAX_REPR_VALUE = 36 ** 7 - 1  # Max number we can represent using a base 36 numeric system with 7 digits


def pk_to_id(n):
    """
    Converts a base 10 integer to an unique identifier following the format:
    TR[NUMBER]
    where NUMBER is the base 10 integer converted to base 36 and padded with 0 on the left to make its total length
    equal 7.
    For example pk_to_uid(1) == TR0000001
    """
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = 36

    try:
        n = int(n)
    except ValueError:
        raise ValueError("number should be an integer")

    if n > UID_MAX_REPR_VALUE:
        raise ValueError("max representable value is {}".format(UID_MAX_REPR_VALUE))

    if n < 0:
        raise ValueError("number should be positive")

    result = ""
    while n > 0:
        r = n % base
        result = digits[r] + result
        n = int(n / base)

    return 'TR{}'.format(result.zfill(7))


def round_decimal(number, decimal_places):
    """
    Rounds the @number Decimal object to @decimal_places
    For example:
        round_decimal(Decimal('100.123466'), 4) returns Decimal('100.1234')
    """
    exp = '.{}1'.format(''.zfill(decimal_places - 1))
    return number.quantize(Decimal(exp), rounding=ROUND_DOWN)
