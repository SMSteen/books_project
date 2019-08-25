from django.db import models
from ..users.models import User
from ..books.models import Book

# Create your models here.
class ReviewManager(models.Manager):
    def review_valid(self, postData):
        errors = {}
        if 'rating' not in postData: # null
            errors['bad_rating'] = "Oops, you forgot to rate the book."
        if len(postData['review']) < 1: # null
            errors['no_review'] = "Oops, you forgot to tell us what you thought of the book."
        elif len(postData['review']) < 3: # not long enough
            errors['bad_review'] = "Hmmm, that doesn't really tell us what you thought of the book. Review should be a minimum of 3 characters."
        # process validations
        return errors

    def create_review(self, postData, user_id):
        reviewer = User.objects.get(id=user_id)
        reviewed_book = Book.objects.get(id=int(postData['book_id']))
        review = self.create(review=postData['review'], rating=int(postData['rating']), reviewer=reviewer, book=reviewed_book)
        return review

class Review(models.Model):
    review = models.TextField()
    rating = models.SmallIntegerField()
    reviewer = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

    def __repr__(self):
        return f'<Review {self.id} - Rating {self.rating}'