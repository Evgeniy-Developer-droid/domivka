

class SEOMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        # print(response, request)
        # response.context_data['custom'] = 'test'
        return response
