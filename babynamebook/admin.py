from django.contrib import admin
from .models import Book, Person, Name
# from django.contrib.auth import authenticate, login

admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Name)


# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     # else:
#     #     # Return an 'invalid login' error message.
#     #     ...
