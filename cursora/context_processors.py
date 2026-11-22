from django.conf import settings


def company_context(request):
    return {
        'date_firma': settings.DATE_FIRMA,
        'ip_client': getattr(request, 'client_ip', 'necunoscut'),
    }
