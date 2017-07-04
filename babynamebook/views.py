from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm
from .utils import parse_ged, parse_xml
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Book, Person

def home(request):
    return render(request, 'babynamebook/home.html', {})

def upload_tree(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book(tree_upload=request.FILES['tree_upload'], title=request.POST['title'])
            # book = form.save(commit=False)
            # add stuff about user
            # print("--------book is: ", book)
            book.save()
            # print("-----book tree upload is :", book.tree_upload.name)
            filename = book.tree_upload.name
            # print("--------DATA IS: ", filename)
            xml_filename = parse_ged(filename)
            person_list = parse_xml(xml_filename)
            for person in person_list:
                new_person = Person(first_name = person["first_name"], last_name = person["last_name"], birth_year = person["birth_year"])
                new_person.book = book
                if new_person.save:
                    print("saved %s" % (new_person))
                else:
                    print("couldn't save")
        return redirect('progress', {'pk': book.pk})
            # return redirect('home', {})
    else:
        form = BookForm()
    return render(request, 'babynamebook/upload_tree.html', {'form': form})

def progress(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'babynamebook/progress.html', {'book': book})
