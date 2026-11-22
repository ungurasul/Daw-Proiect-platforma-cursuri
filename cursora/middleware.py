from .views import Accesare, client_ip


class ClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.client_ip = client_ip(request)
        if not request.path.startswith(('/static/', '/media/', '/admin/')):
            request.accesare = Accesare(request)
            print(request.accesare)
        return self.get_response(request)
