from django.shortcuts import render, redirect
from django.contrib import messages
from ..login_reg.decorators import required_login
from .models import Author


# display listing of all authors
@required_login
def index(request):
    print('authors index method, redering index.html with authors data')
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'authors/index.html', context)


# render form to add new author
@required_login
def new(request):
    print('authors new method, rendering new.html')
    return render(request, 'authors/new.html')


# save new author to database
@required_login
def create(request):
    print('authors create method, adding new  to db')
    errors = Author.objects.author_valid(request.POST)
    if errors:
        for category, error in errors.items():
            messages.error(request, error, extra_tags = category)
        return redirect('/authors/new')
    else:
        author = Author.objects.create_author(request.POST)
        return redirect('/books')


# display one author
@required_login
def show(request, id):
    print('authors show method, rendering show.html with author data')
    context = {
        'author': Author.objects.get(id=id)
    }
    return render(request, 'authors/show.html', context)

