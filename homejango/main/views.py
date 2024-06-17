from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

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


class ReviewsListView(ListView):
    model = Reviews
    context_object_name = 'reviews'
    template_name = 'main/reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewsForms()
        return context


class ReviewCreateView(CreateView):
    model = Reviews
    form_class = ReviewsForms
    template_name = 'main/reviews.html'
    success_url = reverse_lazy('reviews-list')  # URL для перенаправления после создания отзыва

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Reviews.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

#
# def reviews(request):
#     if request.POST:
#         temp_name = request.POST['name']
#         temp_description = request.POST['description']
#         reviews_obj = Reviews(name=temp_name, description=temp_description)
#         reviews_obj.save()
#
#     form = ReviewsForms()
#     reviews = Reviews.objects.all()
#     context = {
#         'reviews': reviews,
#         'form': form
#
#     }
#     return render(request, 'main/reviews.html', context)


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


def personal_doctor(request):
    return render(request, 'main/personal_doctor.html')


def gruming(request):
    return render(request, 'main/gruming.html')
