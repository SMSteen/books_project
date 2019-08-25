from django.db import models
from ..users.models import User
from ..authors.models import Author

# Create your models here.
class BookManager(models.Manager):
    def book_valid(self, postData):
        errors = {}
        if len(postData['title']) < 1: # null
            errors['bad_title'] = "Oops, you forgot to enter the title of the book."
        if 'author' not in postData: # null
            errors['bad_author'] = "Oops, you forgot to choose an author. If the author is not available, add one."
        if len(postData['description']) < 1: # null
            errors['no_desc'] = "Oops, you forgot to describe the book."
        elif len(postData['description']) < 5: # not long enough
            errors['bad_desc'] = "Hmmm, that doesn't tell us much about the book. Description should be a minimum of 5 characters."
        return errors
    
    def create_book(self, postData, user_id):
        # get the user
        user = User.objects.get(id=user_id)
        # get the author
        author = Author.objects.get(id=postData['author'])
        # create the book
        book = self.create(title=postData['title'], author=author, description=postData['description'], uploaded_by_id=user)
        # add the relationship
        book.users_who_like.add(user)
        return book

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by_id = models.ForeignKey(User, related_name="uploaded_books")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    objects = BookManager()

    def __repr__(self):
        return f'<Book {self.id} - Title: {self.title}>'