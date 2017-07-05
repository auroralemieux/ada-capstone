from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
from django.core.urlresolvers import reverse
from babynamebook.forms import BookForm
import unittest
from selenium import webdriver

# models test
class BookTest(TestCase):
    # don't know how to test the FileField
    def create_book(self, title="test_book", upload_tree="WHAT GOES HERE??"):
        return Book.objects.create(title=title, upload_tree=upload_tree)

    # what is the unicode part?
    def test_book_creation(self):
        b = self.create_book()
        self.assertTrue(isinstance(b, Book))
        self.assertEqual(b.__unicode__(), b.title)


    # views (uses reverse)

    def test_home_view(self):
        w = self.create_whatever()
        url = reverse("whatever.views.whatever")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(w.title, resp.content)



class TestHome(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_home_chrome(self):
        self.driver.get("http://127.0.0.1:8000/")
        # self.driver.find_element_by_id('id_title').send_keys("test title")
        # self.driver.find_element_by_id('id_body').send_keys("test body")
        self.driver.find_element_by_id('start-button').click()
        self.assertIn("http://127.0.0.1:8000/upload_tree", self.driver.current_url)

    def tearDown(self):
        self.driver.quit

class TestUploadTree(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_home_chrome(self):
        self.driver.get("http://127.0.0.1:8000/upload_tree")
        self.driver.find_element_by_id('id_title').send_keys("test-book-title")
        # what do I put in the file upload field to test it??
        self.driver.find_element_by_id('id_tree_upload').send_keys("../media/uploads/aurora-tree.ged")
        self.driver.find_element_by_id('start-button').click()
        self.assertIn("http://127.0.0.1:8000/progress", self.driver.current_url)

    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()
