from django.shortcuts import render, redirect
from django.contrib import messages
from ..login_reg.decorators import required_login
from .models import Book
from ..authors.models import Author
from ..users.models import User

# display listing of all books
@required_login
def index(request): 
    print('books index method, rendering index.html')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    logged_in_user_likes = logged_in_user.liked_books.all()
    books_liked = []
    for book in logged_in_user_likes:
        books_liked.append(book.id)
    print('liked books list', books_liked)
    context = {
        'authors': Author.objects.all(),
        'books': Book.objects.all(),
        'likes': books_liked
    }
    return render(request, 'books/index.html', context)


# save new book to database
@required_login
def create(request):
    print('books create method, adding new book to db')
    errors = Book.objects.book_valid(request.POST)
    if errors:
        for category, error in errors.items():
            messages.error(request, error, extra_tags = category)
        return redirect('/books')
    else:
        book = Book.objects.create_book(request.POST, request.session['user_id'])
        return redirect('/books')


# render form to edit selected book
@required_login
def edit(request, id):
    print('books edit method, rendering edit.html with book data')
    context = {
        'book': Book.objects.get(id=id),
        'authors': Author.objects.all(),
    }
    return render(request, 'books/edit.html', context)


# save changes to book in database
@required_login
def update(request, id):
    print('books update method, sending book updates to db')
    errors = Book.objects.book_valid(request.POST)
    if errors:
        for category, error in errors.items():
            messages.error(request, error, extra_tags = category)
        return redirect(f'/books/{id}/edit')
    else:
        book_to_change = Book.objects.get(id=id)
        book_new_author = Author.objects.get(id=int(request.POST['author']))
        book_to_change.title = request.POST['title']
        book_to_change.author = book_new_author
        book_to_change.description = request.POST['description']
        book_to_change.save()
    return redirect(f'/books/{id}')


# display details of selected book
@required_login
def show(request, id):
    print('books show method, redering show.html with book data')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    logged_in_user_likes = logged_in_user.liked_books.all()
    books_liked = []
    for book in logged_in_user_likes:
        books_liked.append(book.id)
    context = {
        'book': Book.objects.get(id=int(id)),
        'likes': books_liked
    }
    return render(request, 'books/show.html', context)


# delete a book
@required_login
def destroy(request, id):
    print('books delete method, deleting book from db')
    book_to_del = Book.objects.get(id=id)
    book_to_del.delete()
    return redirect('/books')


# add a book to user favorites
@required_login
def like(request, id):
    previous_page = request.META['HTTP_REFERER']
    logged_in_user = User.objects.get(id=request.session['user_id'])
    liked_book = Book.objects.get(id=id)
    liked_book.users_who_like.add(logged_in_user)
    return redirect(previous_page)


# remove a book from user favorites
@required_login
def unlike(request, id):
    previous_page = request.META['HTTP_REFERER']
    logged_in_user = User.objects.get(id=request.session['user_id'])
    unliked_book = Book.objects.get(id=id)
    unliked_book.users_who_like.remove(logged_in_user)
    return redirect(previous_page)
