from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm
from .utils import parse_ged, parse_xml
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from .models import Book, Person, Name
import operator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .generate_pdf import go


# maybe put this in a separate accounts project views file???
def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home') # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form

    return render(request, 'registration/signup.html', {'form': form,})

@login_required
def account(request):
    books = Book.objects.filter(author=request.user)
    user = request.user
    return render(request, 'babynamebook/account.html', {'books': books, 'user': user})


@login_required
def book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    persons = Person.objects.filter(book=book)

    # querysets
    all_boys = __get_all_names_for_book_by_gender(book, "M")
    all_girls = __get_all_names_for_book_by_gender(book, "F")
    all_boys = sorted(all_boys.items())
    all_girls = sorted(all_girls.items())

    # querysets
    male = Person.objects.filter(book=book, gender="M")
    female = Person.objects.filter(book=book, gender="F")

    # these are querysets
    top_female = __top_ten_first_names(female, book)
    top_male = __top_ten_first_names(male, book)
    top_last = __top_ten_last_names(persons, book)
    top_origin = __top_five_origins(book)

    # these are lists of strings
    pop_boy_names = __get_popular_names_2016("M", book)
    pop_girl_names = __get_popular_names_2016("F", book)

    book_data = {
        "title": book.title,
        "stats": {
            "top_female": [],
            "top_male": [],
            "top_origin": [],
            "top_last": [],
            "pop_female": [],
            "pop_male": [],
        },
        "boys": {},
        "girls": {},
    }
    book_stats = book_data["stats"]
    if len(pop_boy_names) is not 0:
        for name in pop_boy_names:
            book_stats["pop_male"].append(name)
    if len(pop_girl_names) is not 0:
        for name in pop_girl_names:
            book_stats["pop_female"].append(name)
    for name, num in top_female:
        book_stats["top_female"].append(name)
    for name, num in top_male:
        book_stats["top_male"].append(name)
    for name, num in top_origin:
        book_stats["top_origin"].append(name)
    for name, num in top_last:
        book_stats["top_last"].append(name)

    book_data["stats"] = book_stats
    book_boys = book_data["boys"]
    for letter, names in all_boys:
        book_boys[letter] = []
        for name in names:
            new_name = {
                "first_name": name.first_name,
                "origin": name.origin,
                "meaning": name.meaning,
            }
            book_boys[letter].append(new_name)
    book_girls = book_data["girls"]
    for letter, names in all_girls:
        book_girls[letter] = []
        for name in names:
            new_name = {
                "first_name": name.first_name,
                "origin": name.origin,
                "meaning": name.meaning,
            }
            book_girls[letter].append(new_name)
    print("book data keys: ")
    print(book_data.keys())

    if request.method == "POST":
        go(book_data)
        fs = FileSystemStorage()
        filename = 'babynamebook.pdf'
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="mybabynamebook.pdf"'
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')


    return render(request, 'babynamebook/book.html', {'book': book, 'persons': persons, 'all_girls': all_girls, 'all_boys': all_boys, 'top_female': top_female, 'top_male': top_male, 'top_last': top_last, 'top_origin': top_origin, 'pop_girl_names': pop_girl_names,'pop_boy_names': pop_boy_names, 'book_data': book_data })


def home(request):
    names = Name.objects.all()
    male = len(Name.objects.filter(gender="M"))
    female = len(Name.objects.filter(gender="F"))
    len_names = len(names)
    return render(request, 'babynamebook/home.html', {'names': names, 'male': male, 'female': female, 'len_names': len_names})


def get_tree_instructions(request):
    return render(request, 'babynamebook/get_tree_instructions.html', {})

@login_required
def upload_tree(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book(tree_upload=request.FILES['tree_upload'], title=request.POST['title'])
            # add stuff about user
            book.author = request.user
            book.save()
            filename = book.tree_upload.name
            xml_filename = parse_ged(filename)

            # person_list is an array of dictionary objects
            person_list = parse_xml(xml_filename)
            request.session["book_id"] = book.id
            __parse_person(request, person_list)

        return redirect('progress')
    else:
        form = BookForm()
    return render(request, 'babynamebook/upload_tree.html', {'form': form})


@login_required
def progress(request):
    book = get_object_or_404(Book, id=request.session["book_id"])
    persons = Person.objects.filter(book=book)

    __assoc_first_with_book(book,persons)
    __assoc_middle_with_book(book,persons)

    total_persons = len(persons)
    female = Person.objects.filter(book=book, gender="F")
    male = Person.objects.filter(book=book, gender="M")
    num_m = len(male)
    num_f = len(female)

    return render(request, 'babynamebook/progress.html', {'book': book, 'persons': persons, 'total_persons': total_persons, 'num_m': num_m, 'num_f': num_f, })


# these are private helper methods
def __parse_person(request, person_list):
    for p in person_list:
        new_person = Person(first_name=p["first_name"], last_name=p["last_name"], gender=p["sex"], birth_year=p["birth_year"], )

        if p["last_name"] is None:
            new_person.last_name = "unknown"

        if p["sex"] is None:
            new_person.gender = "x"

        if p["birth_year"] is None:
            new_person.birth_year = 0
        book = get_object_or_404(Book, id=request.session["book_id"])

        new_person.book = book
        new_person.save()


def __assoc_first_with_book(book, person_list):
    for p in person_list:
        try:
            first = Name.objects.get(first_name = p.first_name, gender=p.gender)
            book.names.add(first)

        except Name.DoesNotExist:
            continue


def __assoc_middle_with_book(book, person_list):
    for p in person_list:
        if p.middle_name != None:
            try:
                middle = Name.objects.get(first_name = p.middle_name, gender=p.gender)
                book.names.add(middle)

            except Name.DoesNotExist:
                continue


def __top_ten_first_names(person_list, book):
    freq = {}
    for p in person_list:
        if p.first_name.isalpha() and p.first_name != "unknown":
            if p.first_name in freq.keys():
                freq[p.first_name] += 1
            else:
                freq[p.first_name] = 1
    return sorted(freq.items(), key=operator.itemgetter(1), reverse=True)[0:10]


def __top_ten_last_names(person_list, book):
    freq = {}
    for p in person_list:
        if p.last_name.isalpha() and p.last_name != "unknown":
            if p.last_name in freq.keys():
                freq[p.last_name] += 1
            else:
                freq[p.last_name] = 1
    return sorted(freq.items(), key=operator.itemgetter(1), reverse=True)[0:10]


def __top_five_origins(book):
    freq = {}
    for n in book.names.all():
        if n.origin.isalpha() and n.origin != "unknown":
            if n.origin in freq.keys():
                freq[n.origin] += 1
            else:
                freq[n.origin] = 1
    return sorted(freq.items(), key=operator.itemgetter(1), reverse=True)[0:5]


def __get_all_names_for_book_by_gender(book, gender):
    all_names = {}
    letter = "A"
    for p in range(26):
        all_names[letter] = book.names.all().filter(gender=gender, first_name__startswith=letter).order_by('first_name')
        letter = chr(ord(letter) + 1)
    return all_names

def __get_popular_names_2016(gender, book):
    # from https://www.ssa.gov/oact/babynames/
    pop_results = []
    if gender == "M":
        pop_names = ["Noah", "Liam", "William", "Mason", "James", "Benjamin", "Jacob", "Michael", "Elijah", "Ethan"]
    elif gender == "F":
        pop_names = ["Emma", "Olivia", "Ava", "Sophia", "Isabella", "Mia", "Charlotte", "Abigail", "Emily", "Harper"]

    for n in pop_names:
        try:
            name = book.names.all().get(gender=gender, first_name=n)
            pop_results.append(n)

        except Name.DoesNotExist:
            continue


    return pop_results

def __create_book_data(datablob):
    
