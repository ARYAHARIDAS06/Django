from .models import Category

def links(request):
    ca=Category.objects.all()
    return {'links':ca }