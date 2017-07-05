from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
from django.core.urlresolvers import reverse
from babynamebook.forms import BookForm
import unittest



# ---- FORMS TESTING -----
def test_valid_form(self):
    B = Book.objects.create(title='TEST-title', upload_tree='WHAT GOES HERE???')
    data = {'title': b.title, 'upload_tree': b.upload_tree,}
    form = BookForm(data=data)
    self.assertTrue(form.is_valid())

def test_invalid_form(self):
    b = Book.objects.create(title='testing', upload_tree='')
    data = {'title': b.title, 'upload_tree': b.upload_tree,}
    form = BookForm(data=data)
    self.assertFalse(form.is_valid())
