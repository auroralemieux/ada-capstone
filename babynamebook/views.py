from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm
from .utils import parse_ged, parse_xml
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Book, Person, Name
import operator
import plotly
from plotly.graph_objs import Scatter, Layout
from django.contrib.auth.decorators import login_required


# def login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # Redirect to a success page.
#
#         else:
#             # Return an 'invalid login' error message.
#             print("invalid login")
#     else:
#         print("should get the regular login form")


def home(request):
    names = Name.objects.all()
    male = len(Name.objects.filter(gender="M"))
    female = len(Name.objects.filter(gender="F"))
    len_names = len(names)
    return render(request, 'babynamebook/home.html', {'names': names, 'male': male, 'female': female, 'len_names': len_names})


def get_tree_instructions(request):
    return render(request, 'babynamebook/get_tree_instructions.html', {})


def upload_tree(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book(tree_upload=request.FILES['tree_upload'], title=request.POST['title'])
            # add stuff about user
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


def progress(request):
    book = get_object_or_404(Book, id=request.session["book_id"])
    persons = Person.objects.filter(book=book)
    total_persons = len(persons)
    female = Person.objects.filter(book=book, gender="F")
    male = Person.objects.filter(book=book, gender="M")
    num_m = len(male)
    num_f = len(female)

    return render(request, 'babynamebook/progress.html', {'book': book, 'persons': persons, 'total_persons': total_persons, 'num_m': num_m, 'num_f': num_f, })

def correlate(request):
    book = get_object_or_404(Book, id=request.session["book_id"])
    persons = Person.objects.filter(book=book)

    __assoc_first_with_book(book,persons)
    __assoc_middle_with_book(book,persons)

    all_boys = __get_all_names_for_book_by_gender(book, "M")
    all_girls = __get_all_names_for_book_by_gender(book, "F")

    male = Person.objects.filter(book=book, gender="M")
    female = Person.objects.filter(book=book, gender="F")

    top_female = __top_ten_first_names(female, book)
    top_male = __top_ten_first_names(male, book)
    top_last = __top_ten_last_names(persons, book)
    top_origin = __top_five_origins(book)
    pop_boy_names = __get_popular_names_2016("M", book)
    pop_girl_names = __get_popular_names_2016("F", book)


    return render(request, 'babynamebook/correlate.html', {'book': book, 'persons': persons, 'all_girls': sorted(all_girls.items()), 'all_boys': sorted(all_boys.items()), 'top_female': top_female, 'top_male': top_male, 'top_last': top_last, 'top_origin': top_origin, 'pop_girl_names': pop_girl_names,'pop_boy_names': pop_boy_names})


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
