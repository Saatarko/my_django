from django.shortcuts import render

# Create your views here.
def index(request):
    date ={
        'title': 'Домашняя страница',
        'values': ['Some','Hello','oga']
    }
    return render(request, 'main/index.html', date)

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')
