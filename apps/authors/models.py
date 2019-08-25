from django.db import models
import re #for testing/matching regular expressions
NAME_REGEX = re.compile(r'[\sa-zA-Z.-]{2,}$') #regex to confirm only letters, dashes, periods and spaces included in name and minimum of 2 characters

# Create your models here.
class AuthorManager(models.Manager):
    def author_valid(self, postData):
        errors={}
        if not NAME_REGEX.match(postData['first_name']):  #null or invalid
            errors['bad_first'] = "Please enter the author's first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['last_name']):  #null or invalid      
            errors['bad_last'] = "Please enter the author's last name, ensuring invalid characters (numbers, symbols) are not included."
        return errors
    
    def create_author(self, postData):
        author = self.create(first_name=postData['first_name'], last_name=postData['last_name'], notes=postData['notes'])
        return author

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

    def __repr__(self):
        return f'<Author {self.id} - {self.first_name} {self.last_name}>'