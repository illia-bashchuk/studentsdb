#from .settings import PORTAL_URL
#a = 'as'
def students_processors(request):
    HTTP_HOST = request.scheme + '://' + request.META['HTTP_HOST']
    return {'PORTAL_URL': HTTP_HOST}
