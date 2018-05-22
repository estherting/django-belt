from django.db import models
import datetime
import bcrypt

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name should be at least 3 characters"
        if User.objects.filter(username=postData['username']):
            errors['username'] = "Username already in use. Please choose a different username."
        if len(postData['username']) < 3:
            errors['username'] = "Username should be at least 3 characters"
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and Confirm password must match"
        return errors

    def validate_signin(self, postData):
        errors = {}
        if postData['username']:
            try:
                user = User.objects.get(username=postData['username'])
                if not user:
                    errors['login'] = "Unable to signin"
                elif not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                    errors['login'] = "Unable to signin"
            except:
                errors['login'] = "Unable to signin"
        else:
            errors['login'] = "Unable to signin"
        return errors

    def validate_trip(self, postData):
        errors = {}

        return errors


class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    planned_by = models.ForeignKey(User, related_name="trips_planned")
    attended_by = models.ManyToManyField(User, related_name="trips_attending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
