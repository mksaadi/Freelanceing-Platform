from selenium import webdriver
from posts.models import Job
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class TestJobListPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_test/chromedriver.exe')


    def tearDown(self):
        self.browser.close()


    def home_page(self):
        self.browser.get(self.live_server_url)
        time.sleep(20)
