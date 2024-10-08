from django.contrib.auth.models import User

from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import IntegrationTest
from .factories import UserProfileFactory

from .utils import scroll_and_click


class UserAuthTest(IntegrationTest):
    def test_register_a_new_account(self):
        url = self.live_server_url + reverse("register")
        self.browser.get(url)

        self.browser.find_element(By.NAME, "username").send_keys("test_user")
        self.browser.find_element(By.NAME, "email").send_keys("test_user@domain.com")
        self.browser.find_element(By.NAME, "password1").send_keys(
            "super_secret_pwd_1234"
        )
        self.browser.find_element(By.NAME, "password2").send_keys(
            "super_secret_pwd_1234"
        )

        register_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='register']"))
        )
        scroll_and_click(browser=self.browser, element=register_button)

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse("tweet_home")
        self.assertEqual(self.browser.current_url, expected_url)

    def test_login_with_new_account(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="super_secret_pwd_1234",
        )

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse("tweet_home")
        self.assertEqual(self.browser.current_url, expected_url)

    def test_logout(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="super_secret_pwd_1234",
        )
        UserProfileFactory.logout_user(browser=self.browser)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@name='logout']"))
        )

        self.assertTrue(
            EC.element_to_be_clickable((By.XPATH, "//button[@name='login']"))
        )

    def test_change_password(self):
        UserProfileFactory.create_user(
            username='test_user', password='super_secret_pwd_1234', email='test_user@domain.com'
        )
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="super_secret_pwd_1234",
        )
        UserProfileFactory.create_profile_for_test_user(username="test_user")
        UserProfileFactory.go_to_user_profile(browser=self.browser)

        change_pwd_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@name='change_pwd_btn']"))
        )
        scroll_and_click(browser=self.browser, element=change_pwd_btn)

        change_pwd_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@name='change_pwd_btn']"))
        )

        self.browser.find_element(By.XPATH, "//input[@name='old_password']").send_keys("super_secret_pwd_1234")
        self.browser.find_element(By.XPATH, "//input[@name='new_password1']").send_keys("new_secret_pwd_6789")
        self.browser.find_element(By.XPATH, "//input[@name='new_password2']").send_keys("new_secret_pwd_6789")

        scroll_and_click(browser=self.browser, element=change_pwd_btn)

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        self.assertEqual(
            self.browser.find_element(By.CLASS_NAME, "alert").text,
            "Your password was successfully updated!",
        )

        UserProfileFactory.logout_user(browser=self.browser)
        UserProfileFactory.login_user(
            browser=self.browser,
            live_server_url=self.live_server_url,
            username="test_user",
            password="new_secret_pwd_6789",
        )

        WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))

        expected_url = self.live_server_url + reverse("tweet_home")
        self.assertEqual(self.browser.current_url, expected_url)
