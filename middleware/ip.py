from middleware.models import IpAddress, UserIps

import datetime


class SaveIpAddressMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.get_response(request)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        ip_address = IpAddress(
            ip_address=ip,
            pub_date=datetime.datetime.now(),
            method=request.method,
            url=request.path
        )
        ip_address.save()

        UserIps(user=request.user, ip=ip_address).save()

        return self.get_response(request)
