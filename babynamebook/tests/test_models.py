from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from babynamebook.forms import BookForm
import mock
from django.core.files import File
from django.core.files.storage import Storage


class BookTest(TestCase):
    # don't know how to test the FileField
    # def create_book(self, title="test_book", upload_tree=None):
    #     file_field = SimpleUploadedFile('my_tree.ged', 'these are the file contents!')
    #     return Book.objects.create(title=title, upload_tree=file_field)

    # what is the unicode part?
    def test_book_creation(self):
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.jpg'

        book = Book(title="test-book")
        book.upload_tree = file_mock

        storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        storage_mock.url = mock.MagicMock(name='url')
        storage_mock.url.return_value = '/tmp/test1.jpg'

        with mock.patch('django.core.files.storage.default_storage._wrapped', storage_mock):
            book.save()

        self.assertTrue(isinstance(book, Book))
        self.assertEqual("test-book", book.title)

    # def test_string_method(self):
    #     b = self.create_book()
    #     self.assertEqual(b.__string__(), b.title)
