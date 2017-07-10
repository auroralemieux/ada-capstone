from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from babynamebook.forms import BookForm
import mock
from django.core.files import File
from django.core.files.storage import Storage
from django.test import Client


class BookTest(TestCase):

    ## this is NOT passing!!!!!
    def test_book_creation(self):

        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.ged'

        book = Book(title="test-book")
        book.upload_tree = file_mock
        book.author = user
        storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        storage_mock.url = mock.MagicMock(name='url')
        storage_mock.url.return_value = '/tmp/test1.ged'

        with mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock):
            book.save()

        self.assertTrue(isinstance(book, Book))
        self.assertEqual("test-book", book.title)

    def test_book_string_method(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.ged'

        book = Book(title="test-book")
        book.upload_tree = file_mock
        book.author = user

        storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        storage_mock.url = mock.MagicMock(name='url')
        storage_mock.url.return_value = '/tmp/test1.ged'

        with mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock):
            book.save()

        self.assertEqual(book.__str__(), book.title)

class PersonTest(TestCase):

    ## this is passing!!!!!
    def test_person_creation(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.ged'

        book = Book(title="test-book")
        book.upload_tree = file_mock
        book.author = user

        storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        storage_mock.url = mock.MagicMock(name='url')
        storage_mock.url.return_value = '/tmp/test1.ged'

        with mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock):
            book.save()

        self.assertTrue(isinstance(book, Book))

        person = Person(book=book, first_name="first", middle_name="middle", last_name="last", birth_year=1982, gender="F")
        self.assertTrue(isinstance(person, Person))

        self.assertEqual("first", person.first_name)

    def test_person_string_method(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.ged'

        book = Book(title="test-book")
        book.upload_tree = file_mock
        book.author = user

        storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        storage_mock.url = mock.MagicMock(name='url')
        storage_mock.url.return_value = '/tmp/test1.ged'

        with mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock):
            book.save()

        self.assertTrue(isinstance(book, Book))

        person = Person(book=book, first_name="first", middle_name="middle", last_name="last", birth_year=1982, gender="F")

        self.assertEqual(person.__str__(), "first last (1982)")

class NameTest(TestCase):

    def test_name_creation(self):

        name = Name(first_name="first", origin="French", gender="F", meaning="test")
        self.assertTrue(isinstance(name, Name))

        self.assertEqual("first", name.first_name)

    def test_name_string_method(self):

        name = Name(first_name="first", origin="French", gender="F", meaning="test")

        self.assertEqual(name.__str__(), "first")
