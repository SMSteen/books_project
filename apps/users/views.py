from django.shortcuts import render, redirect
from ..login_reg.decorators import required_login
from django.contrib import messages
from .models import User

# Create your views here.
@required_login
def show(request, id):
    print('users show method, rendering show.html with user data')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    uploaded_books = logged_in_user.uploaded_books.all()
    reviewed_books = logged_in_user.reviews.all()
    users_books = []
    users_reviews = []
    for book in uploaded_books:
        users_books.append(book.id)
    for review in reviewed_books:
        users_reviews.append(review.book.id)
    print(users_reviews)
    context = {
        'user': logged_in_user,
        'users_books_ids': users_books,
        'reviewed_books': reviewed_books,
        'users_reviews_id': users_reviews
    }
    return render(request, 'users/show.html', context)

@required_login
def edit(request, id):
    print('users edit method, rendering edit.html with  data')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'users/edit.html', context)

@required_login
def update(request, id):
    print('users update method, sending updates to db')
    previous_page = request.META['HTTP_REFERER']
    errors = User.objects.profile_valid(request.POST)
    print(errors)
    if errors:
        for category, error in errors.items():
            messages.error(request, error, extra_tags = category)
        return redirect(previous_page)
    else:
        User.objects.update_user(request.POST, id)
        return redirect(f'/users/{id}')
