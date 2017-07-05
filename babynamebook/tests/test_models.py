from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
import unittest

class BookTest(TestCase):
    # don't know how to test the FileField
    def create_book(self, title="test_book", upload_tree="WHAT GOES HERE??"):
        return Book.objects.create(title=title, upload_tree=upload_tree)

    # what is the unicode part?
    def test_book_creation(self):
        b = self.create_book()
        self.assertTrue(isinstance(b, Book))
        self.assertEqual(b.__unicode__(), b.title)
