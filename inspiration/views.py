from django.shortcuts import render, get_object_or_404
from .models import Inspiration

# Create your views here.'

def inspiration(request):
    inspirations = Inspiration.objects.all()
    context = {
        'inspirations':inspirations
    }
    return render(request, 'articles/inspiration.html', context)

# def inspiration_detail(request, slug):
#     inspiration = get_object_or_404(Inspiration, slug=slug)
#     context = {
#         'inspiration':inspiration
#     }
#     return render(request, 'inspiration/inspiration.html', context)
