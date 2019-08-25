from django.shortcuts import render, redirect
from django.contrib import messages
from ..login_reg.decorators import required_login
from .models import Book
from ..users.models import User
from .models import Review

# Create your views here.
@required_login
def create(request):
    print('reviews create method, adding new review to db')
    previous_page = request.META['HTTP_REFERER']
    errors = Review.objects.review_valid(request.POST)
    if errors:
        for category, error in errors.items():
            messages.error(request, error, extra_tags=category)
    else:
        review = Review.objects.create_review(request.POST, request.session['user_id'])
    return redirect(previous_page)





