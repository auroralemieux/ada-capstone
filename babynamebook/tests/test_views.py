from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
from django.core.urlresolvers import reverse
import unittest
from selenium import webdriver
import os
from noseselenium.cases import SeleniumTestCaseMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# HOW DO / SHOULD I TEST PRIVATE METHODS IN VIEWS?

# ---- VIEWS TESTING WITH SELENIUM WEBDRIVER  -----
# this test is working
# what else should I be testing?
class TestHome(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def test_home_chrome(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element_by_link_text("babynamebook")
        self.driver.find_element_by_id("start-button")

    def tearDown(self):
        self.driver.close()

# really no idea what this test should look like
# help!!!
class TestGetTreeInstructions(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def test_get_tree_instructions_chrome(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element_by_id("start-button").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/get_tree_instructions/')

    def tearDown(self):
        self.driver.close()


class TestUploadTreeNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def test_upload_tree_not_logged_in_chrome(self):
        self.driver.get("http://127.0.0.1:8000/get_tree_instructions/")
        self.driver.find_element_by_id("instructions-button").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/accounts/login/?next=/upload_tree/')

    def tearDown(self):
        self.driver.close()


class TestGetUploadTreeLoggedIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def login(self, username="test", password="xueimel1", next_url=None):

        self.driver.get("http://127.0.0.1:8000/accounts/login/")

        username_el = self.driver.find_element_by_id("id_username")
        username_el.send_keys(username)
        password_el = self.driver.find_element_by_id("id_password")
        password_el.send_keys(password)

        if next_url:
            el = self.driver.find_element_by_name("next")
            self.set_element_attribute(el, "value", next_url)

        self.driver.find_element_by_css_selector("form").submit()

    def test_get_upload_tree_logged_in_chrome(self):
        self.login()
        self.driver.get("http://127.0.0.1:8000/get_tree_instructions/")
        self.driver.find_element_by_id("instructions-button").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/upload_tree/')

    def tearDown(self):
        self.driver.close()


class TestAccountLoggedIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def login(self, username="test", password="xueimel1", next_url=None):

        self.driver.get("http://127.0.0.1:8000/accounts/login/")

        username_el = self.driver.find_element_by_id("id_username")
        username_el.send_keys(username)
        password_el = self.driver.find_element_by_id("id_password")
        password_el.send_keys(password)

        if next_url:
            el = self.driver.find_element_by_name("next")
            self.set_element_attribute(el, "value", next_url)

        self.driver.find_element_by_css_selector("form").submit()

    def test_account_logged_in_chrome(self):
        self.login()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element_by_id("account-button").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/account/')

    def tearDown(self):
        self.driver.close()

class TestUploadTreeLoggedIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')



    def login(self, username="test", password="xueimel1", next_url=None):

        self.driver.get("http://127.0.0.1:8000/accounts/login/")
        username_el = self.driver.find_element_by_id("id_username")
        username_el.send_keys(username)
        password_el = self.driver.find_element_by_id("id_password")
        password_el.send_keys(password)

        if next_url:
            el = self.driver.find_element_by_name("next")
            self.set_element_attribute(el, "value", next_url)

        self.driver.find_element_by_css_selector("form").submit()

    def test_upload_tree_logged_in_chrome(self):
        self.login()
        self.driver.get("http://127.0.0.1:8000/upload_tree/")

        book_title_el = self.driver.find_element_by_id("id_title")
        book_title_el.send_keys("test_title")
        file_name_el = self.driver.find_element_by_id("id_tree_upload")

        dir = os.path.dirname(__file__)
        tree_upload_path = dir + "/small-tree.ged"

        file_name_el.send_keys(tree_upload_path)
        self.driver.find_element_by_css_selector("form").submit()
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.current_url != "http://127.0.0.1:8000/upload_tree/")

        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/progress/')


    def tearDown(self):
        self.driver.close()

class TestProgressLoggedIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')


    def login(self, username="test", password="xueimel1", next_url=None):

        self.driver.get("http://127.0.0.1:8000/accounts/login/")
        username_el = self.driver.find_element_by_id("id_username")
        username_el.send_keys(username)
        password_el = self.driver.find_element_by_id("id_password")
        password_el.send_keys(password)

        if next_url:
            el = self.driver.find_element_by_name("next")
            self.set_element_attribute(el, "value", next_url)

        self.driver.find_element_by_css_selector("form").submit()

    def upload_tree(self):
        self.login()
        self.driver.get("http://127.0.0.1:8000/upload_tree/")

        book_title_el = self.driver.find_element_by_id("id_title")
        book_title_el.send_keys("test_title")
        file_name_el = self.driver.find_element_by_id("id_tree_upload")

        dir = os.path.dirname(__file__)
        tree_upload_path = dir + "/small-tree.ged"

        file_name_el.send_keys(tree_upload_path)
        self.driver.find_element_by_css_selector("form").submit()
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.current_url != "http://127.0.0.1:8000/upload_tree/")

        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/progress/')

    def test_progress_logged_in_chrome(self):
        self.upload_tree()
        self.driver.find_element_by_id("correlate-button").click()
        download_form_el = self.driver.find_element_by_id("download_form")
        # what else should this test? How do I dynamically test the url?

    def tearDown(self):
        self.driver.close()

class TestUserSignup(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')


    def test_signup(self, username="signup-test", password="newtest1", next_url=None):

        self.driver.get("http://127.0.0.1:8000/accounts/login/")
        self.driver.find_element_by_id("get-signup").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/signup/')

        username_el = self.driver.find_element_by_id("id_username")
        username_el.send_keys(username)
        password_el1 = self.driver.find_element_by_id("id_password1")
        password_el1.send_keys(password)
        password_el2 = self.driver.find_element_by_id("id_password2")
        password_el2.send_keys(password)

        self.driver.find_element_by_id("signup-button").click()

        driver = self.driver
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.current_url != "http://127.0.0.1:8000/signup/")

        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/')

    def tearDown(self):
        self.driver.close()

## use this in a test to see if pdf downloaded
# response = HttpResponse(my_data, content_type='application/vnd.ms-excel')
# response['Content-Disposition'] = 'attachment; filename="foo.xls"'


if __name__ == '__main__':
    unittest.main()
