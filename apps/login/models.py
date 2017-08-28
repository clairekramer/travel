from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = {}
        for field, value in postData.iteritems():
            if len(value) < 1:
                errors[field] = 'All Fields are Required'
        if 'password' not in errors and len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 Characters'
        if 'password' not in errors and postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords do not match'
        if 'name' not in errors and len(postData['name']) < 3:
            errors['name'] = 'Name must be at least 3 Characters'
        if 'username' not in errors and len(postData['username']) < 3:
            errors['username'] = 'Username must be at least 3 Characters'
        if len(errors) == 0:
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = self.create(
                name=postData['name'],
                username=postData['username'],
                password=hashed
            )
            return new_user
        else:
            return errors

    def validate_login(self, postData):
        errors = {}
        if len(self.filter(username = postData['username'])) > 0:
            user = self.filter(username = postData['username'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = 'Incorrect Password'
        else:
            errors['username'] = 'Incorrect Email'
        if errors:
            return errors
        return user

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __repr__(self):
        return 'User: {}'.format(self.name)
