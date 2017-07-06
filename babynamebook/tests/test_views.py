from django.test import TestCase
from babynamebook.models import Book, Person, Name, User
from django.utils import timezone
from django.core.urlresolvers import reverse
import unittest
from selenium import webdriver
import os
from noseselenium.cases import SeleniumTestCaseMixin



# ---- VIEWS TESTING WITH SELENIUM WEBDRIVER  -----

class TestHome(unittest.TestCase):

    # def test_home(self):

        # sel = self.selenium
        # sel.open("http://127.0.0.1:8000/")
        # self.failUnless(sel.is_text_present("babynamebook"))
    def setUp(self):
        self.driver = webdriver.Chrome('babynamebook/chromedriver')

    def test_home_chrome(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element_by_link_text("babynamebook")
        self.driver.find_element_by_id("start-button")



    def tearDown(self):
        self.driver.close()

# class TestUploadTree(unittest.TestCase):
#
#     def setUp(self):
#         self.driver = webdriver.Chrome('babynamebook/chromedriver')
#
#     def test_home_chrome(self):
#         self.driver.get("http://127.0.0.1:8000/upload_tree")
#         self.driver.find_element_by_id('id_title').send_keys("test-book-title")
#         # what do I put in the file upload field to test it??
#         self.driver.find_element_by_id('id_tree_upload').send_keys("../media/uploads/aurora-tree.ged")
#         self.driver.find_element_by_id('start-button').click()
#         self.assertIn("http://127.0.0.1:8000/progress", self.driver.current_url)
#
#     def tearDown(self):
#         self.driver.quit

if __name__ == '__main__':
    unittest.main()
