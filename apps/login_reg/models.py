from django.db import models
import bcrypt #for enctypting passwords
import re #for testing/matching regular expressions
NAME_REGEX = re.compile(r'[\sa-zA-Z.-]{2,}$') #regex to confirm only letters, dashes, periods and spaces included in name and minimum of 2 characters
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #regex for proper email format
PW_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #regex for password, confirm 1 uppercase, 1 num


# Create your models here.
class UserManager(models.Manager):
    def registration_valid(self, postData):
        errors = {}
        if not NAME_REGEX.match(postData['first_name']):  #null or invalid
            errors['bad_first'] = "Please enter your first name, ensuring invalid characters (numbers, symbols) are not included."
        if not NAME_REGEX.match(postData['last_name']):  #null or invalid      
            errors['bad_last'] = "Please enter your last name, ensuring invalid characters (numbers, symbols) are not included."
        
        if not EMAIL_REGEX.match(postData['email']):  #null or invalid      
            errors['bad_email'] = "Please enter a valid email address."
        
        #check if email is already in database
        if User.objects.filter(email=postData['email']): #email already in db
            errors['dup_email'] = "Sorry, that email already exists in the database."

        if len(postData['password']) < 1 or not PW_REGEX.match(postData['password']): #null or invalid
            errors['bad_pw'] = "Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number."
        
        if postData['pwconf'] != postData['password']: #passwords do not match
            errors['bad_pwconf'] = "The password you entered does not match. Please try again."
        
        return errors

    def login_valid(self, postData):
        errors = {}
        try:  
            #search for user based on email address
            user = User.objects.get(email=postData['email'])
            #found one, now confirm password
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()): #passwords do not match
                errors['bad_login'] = "You have entered invalid credentials."
        except User.DoesNotExist: #no user found
                errors['bad_login'] = "You have entered invalid credentials."
        return errors

    def create_user(self, postData):
        enc_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())  #encrypt password
        user = self.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=enc_pw)
        return user

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f'<User {self.id} - {self.first_name} {self.last_name}>'