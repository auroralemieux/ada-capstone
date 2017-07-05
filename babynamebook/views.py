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
            # add stuff about user
            book.save()
            filename = book.tree_upload.name
            xml_filename = parse_ged(filename)
            person_list = parse_xml(xml_filename)

            for p in person_list:
                new_person = Person(first_name=p["first_name"], last_name=p["last_name"], gender=p["sex"], birth_year=p["birth_year"], )
                if p["last_name"] is None:
                    new_person.last_name = "unknown"

                if p["first_name"] is None:
                    new_person.first_name = "unknown"

                if p["sex"] is None:
                    new_person.gender = "x"

                if p["birth_year"] is None:
                    new_person.birth_year = "0000"

                new_person.book = book
                new_person.save()
        book_id = book.pk
        request.session["book_id"] = book_id
        return redirect('progress')
        # return redirect('home')
    else:
        form = BookForm()
    return render(request, 'babynamebook/upload_tree.html', {'form': form})

def progress(request, pk):
    book = get_object_or_404(Book, pk=request.session["book_id"])
    persons = Person.objects.filter(book__value=book)
    print(len(persons))
    # for person in persons[0:2]:
    #     print(person.first_name)
    #     print(person.first_name.name)

    return render(request, 'babynamebook/progress.html', {'book': book, 'persons': persons})
