from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from .forms import ReviewsForms
from .models import Reviews


# Create your views here.
def index(request):
    date = {
        'title': 'Домашняя страница',
    }
    return render(request, 'main/index.html', date)


def about(request):
    return render(request, 'main/about.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def reviews(request):


    if request.POST:
        temp_name = request.POST['name']
        temp_description = request.POST['description']
        reviews_obj = Reviews(name=temp_name, description=temp_description)
        reviews_obj.save()

    form = ReviewsForms()
    reviews = Reviews.objects.all()
    context = {
        'reviews': reviews,
        'form': form

    }
    return render(request, 'main/reviews.html', context)


def reviews_delete(request, id):
    reviews_to_delete = Reviews.objects.filter(id=id)
    reviews_to_delete.delete()

    form = ReviewsForms()
    reviews = Reviews.objects.all()
    context = {
        'reviews': reviews,
        'form': form

    }
    return render(request, 'main/reviews.html', context)
