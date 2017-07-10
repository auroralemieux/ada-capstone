from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
from django.core.urlresolvers import reverse
import unittest
from selenium import webdriver
import os
from noseselenium.cases import SeleniumTestCaseMixin
from django.core.files.uploadedfile import SimpleUploadedFile

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

    # def setUp(self):
    #     self.driver = webdriver.Chrome('babynamebook/chromedriver')
    #
    # def test_home_chrome(self):
    #     self.driver.get("http://127.0.0.1:8000/")
    #     self.driver.find_element_by_link_text("babynamebook")
    #     self.driver.find_element_by_id("start-button").click()
    #
    #     self.driver.get("http://127.0.0.1:8000/get_tree_instructions")
    #
    #
    # def tearDown(self):
    #     self.driver.close()

#
# class TestUploadTree(unittest.TestCase):
#
# class TestProgress(unittest.TestCase):
#
#
# class TestCorrelate(unittest.TestCase):

if __name__ == '__main__':
    unittest.main()
