from django.core.exceptions import PermissionDenied


class NeedToLoginMiddleware(object):
    @staticmethod
    def process_request(request):
        #ip = request.META['REMOTE_ADDR']  # during development

        # MUST HAVE THIS to unmask the IP
        #if 'HTTP_X_FORWARDED_FOR' in request.META:  # load balancer
        #    ip = request.META['HTTP_X_FORWARDED_FOR']

        #white_list = [i.ip for i in IP.objects.all()]
        #if ip not in white_list:  # ip check
        #    if not request.user.is_authenticated():  # if ip check failed, make authentication check
        #        raise PermissionDenied
        return None
