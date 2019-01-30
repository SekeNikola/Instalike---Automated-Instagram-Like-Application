from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from random import randint
import sys
from tkinter import *
from tkinter import ttk
import datetime
import os
stop_time = datetime.datetime.now() + datetime.timedelta(hours=1)
username = ''
password = ''
tag = ''


class GetEntry():
    def __init__(self, master, username, password, tag):
        self.master = master
        master.title("Instalike")
        master.iconbitmap("./assets/favicon.ico")
        self.username_label = ttk.Label(
            master, text="Please enter your Facebook username", font="Arial 10")
        self.username_entry = Entry(master)
        self.password_label = ttk.Label(
            master, text="Please enter your Facebook password", font="Arial 10")
        self.password_entry = Entry(master,  show="*")
        self.tag_label = Label(
            master, text="Enter Hashtag (without #)", font="Arial 10")
        self.tag_entry = Entry(master)
        self.button = ttk.Button(master, text="Start Liking",
                                 command=self.callback)

        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.tag_label.grid(row=2, column=0, padx=10, pady=10)
        self.tag_entry.grid(row=2, column=1, padx=10, pady=10)
        self.button.grid(row=3, column=1, padx=10, pady=10)

        self.statusbar = ttk.Label(master,
                                   text="For any problem send an email to: sekenikola@gmail.com", font="Arial 10 italic")
        self.statusbar.grid(row=4, column=0)

    def callback(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.tag = self.tag_entry.get()
        self.master.destroy()


master = Tk()
GE = GetEntry(master, username, password, tag)
master.mainloop()


class Instalike():
    def __init__(self):
        Options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(
            executable_path='./assets/chromedriver.exe', options=Options)
        self.driver.set_window_position(0, 0)

    def closeBrowser(self):
        self.driver.quit()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_class_name(
            "sqdOP")
        login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath(
            "//input[@name='email']")
        user_name_elem.clear()
        user_name_elem.send_keys(username)
        passworword_elem = driver.find_element_by_xpath(
            "//input[@name='pass']")
        passworword_elem.clear()
        passworword_elem.send_keys(password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(2)
        # Pop Up Confirm
        # not_now_elem = driver.find_element_by_class_name(
        #     "HoLwm"
        # )
        # not_now_elem.click()

        # Check if 1 hour is passed
        if datetime.datetime.now() > stop_time:
            ig.closeBrowser()
            os.system("taskkill /f /im  Instalike.exe")

    def like_photo(self, hashtag):
        driver = self.driver
        time.sleep(2)
        driver.get(
            "https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 17):
            try:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href)
                    for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            pause = randint(12, 20)
            time.sleep(pause)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            try:
                def like_button(): return driver.find_element_by_xpath(
                    '//span[@aria-label="Like"]').click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    time.sleep(second)
            except:
                time.sleep(2)
            unique_photos -= 1
            if datetime.datetime.now() > stop_time:
                ig.closeBrowser()
                os.system("taskkill /f /im  Instalike.exe")


if __name__ == "__main__":
    username = GE.username
    password = GE.password
    ig = Instalike()
    ig.login()
    while True:
        try:
            ig.like_photo(GE.tag)
        except Exception:
            ig.closeBrowser()
