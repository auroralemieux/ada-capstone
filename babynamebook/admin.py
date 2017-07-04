from django.contrib import admin
from .models import Book, Person, Name, User

admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Name)
admin.site.register(User)
