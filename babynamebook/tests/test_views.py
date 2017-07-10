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

    def test_home_chrome(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element_by_id("start-button").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/get_tree_instructions/')

    def tearDown(self):
        self.driver.close()


class TestUploadTreeNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def test_home_chrome(self):
        self.driver.get("http://127.0.0.1:8000/get_tree_instructions/")
        self.driver.find_element_by_id("instructions-button").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/accounts/login/?next=/upload_tree/')

    def tearDown(self):
        self.driver.close()


class TestUploadTreeLoggedIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def test_home_chrome(self):
        c = Client()
        c.login(username='aurora', password='secret')
        self.driver.get("http://127.0.0.1:8000/get_tree_instructions/")
        self.driver.find_element_by_id("instructions-button").click()
        url = self.driver.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/upload_tree/')

    def tearDown(self):
        self.driver.close()


# class TestProgress(unittest.TestCase):
#
#
# class TestCorrelate(unittest.TestCase):

if __name__ == '__main__':
    unittest.main()
