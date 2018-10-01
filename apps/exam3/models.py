from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')
# Create your models here.
class Validate(models.Manager):
    def validate(self,form_data):
        errors = []
        if len(form_data['firstname']) < 1:
            errors.append('first name is required')
        elif len(form_data['firstname']) < 2:
            errors.append('Name must be 2 letters or longer')

        if len(form_data['lastname']) < 1:
            errors.append('last name is required')

        if len(form_data['email']) < 1:
            errors.append('Email is required')
        elif not EMAIL_REGEX.match(form_data['email']):
            errors.append('Invalid Email')
        
        else:
            if len(Reg.objects.filter(email=form_data['email'])):
                errors.append('Email already taken')

        if len(form_data['password'])<1:
            errors.append('Password is required')

        elif len(form_data['password']) < 5:
            errors.append('Password must be 5 Characters or more')

        if len(errors) > 0:
            return(False, errors)
        else:
            return(True,errors)


    def login(self, post_data):
        errors = []

        if len(post_data['email']) < 1:
            errors.append('Email is required')
        elif not EMAIL_REGEX.match(post_data['email']):
            errors.append('Invalid email')
        elif Reg.objects.filter(email=post_data['email']).count() < 1:
            errors.append('This is not an email in the database')

        if len(post_data['password']) < 1:
            errors.append('password is required')
        elif len(post_data['password']) < 4:
            errors.append('password must be 5 characters or longer')

        if len(errors) > 0:
            return(False, errors)
        else: 
            return(True,errors)


    def edit(self, form_data):
        errors = []
        if len(form_data['firstname'])< 1:
            errors.append('firstname is required')
        if len(form_data['lastname'])< 1:
            errors.append('lastname is required')

        if len(errors) > 0:
            return(False, errors)

        else: 

            return(True,errors)


class Reg(models.Model):
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length= 255)
    email = models.CharField(max_length= 255)
    pw_hash = models.CharField(max_length= 255)
    # created_at = models.DateTimeField(auto_now_add = True)
    # updated_at = models.DateTimeField(auto_now = True)
    
    objects = Validate()

class Valid(models.Manager):
    def valid(self,form_data):
        errors = []
        if len(form_data['title']) < 1:
            errors.append('Name is required')
        elif len(form_data['title']) < 3:
            errors.append('Name must have three characters or more')

        if len(form_data['desc']) < 1:
            errors.append('Description is required')  
        elif len(form_data['desc']) < 10:
            errors.append('Description must be 10 characters or longer')

        if len(form_data['location']) < 1:
            errors.append('Location is required')

        if len(errors)>0:
            return(False, errors)
        else:
            return (True,errors)

class Job(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.TextField(max_length = 1000)
    location = models.CharField(max_length = 255)
    jobs = models.ForeignKey(Reg, related_name='job')
    joins = models.ManyToManyField(Reg,related_name = 'jobbers')
    
    objects = Valid()
