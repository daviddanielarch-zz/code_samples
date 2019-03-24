from django.utils.translation.trans_real import parse_accept_lang_header


class AcceptLaguageMiddleware(object):
    """
    Parse the HTTP_ACCEPT_LANGUAGE header and add a new field (USER_LANGUAGE) to request with the user browser's language
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        langs = parse_accept_lang_header(request.META.get('HTTP_ACCEPT_LANGUAGE', ''))
        if langs:
            request.USER_LANGUAGE = langs[0][0]
        else:
            request.USER_LANGUAGE = 'en-US'

        response = self.get_response(request)

        return response
