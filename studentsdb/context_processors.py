# get a dynamic portal URL
def students_processors(request):
    HTTP_HOST = request.scheme + '://' + request.META['HTTP_HOST']
    return {'PORTAL_URL': HTTP_HOST}
