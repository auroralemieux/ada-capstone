from django.db import models
from django.utils import timezone


class Book(models.Model):
    # has many Persons
    # belongs to a User

    # how does this work?
    tree_upload = models.FileField(upload_to='uploads')
    title = models.CharField(max_length=200)
    # user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Person(models.Model):
    # belongs to a Book
    # has a Name
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    name = models.ForeignKey('Name', on_delete=models.PROTECT, related_name="+", blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_year = models.IntegerField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        full_name = "%s %s (%s)" % (self.first_name, self.last_name, self.birth_year)
        return full_name


class Name(models.Model):
    # one-to-many to People
    first_name = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    meaning = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name


class User(models.Model):
    # has many Books
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)

    # uid = models.UUIDField(max_length=200)
    provider = models.CharField(max_length=200)

    def __str__(self):
        return self.username
