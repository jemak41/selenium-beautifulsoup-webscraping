from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re, os, requests, csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import getpass

username = input('Please enter your username: ')
password = getpass.getpass('Please enter your password: ')
url = 'https://mbasic.facebook.com'
url_give = input('Please provide the URL: ')
search = ''

keyword = input('Enter keyword: ')
keywords = keyword.split(',')
pages = 100
page = 1
comment_class_list = 'ec'
comment_class_page1 = 'ee'
comment_class = 'ef'

driver = webdriver.Chrome()
driver.get(url)

if not url_give:
    search = input('Search for: ')


driver.find_element_by_id('m_login_email').send_keys(username)
driver.find_element_by_name('pass').send_keys(password)

button = driver.find_element_by_name('login')
button.click()
python_button = driver.find_element_by_xpath("//input[@type='submit']")
python_button.click()

if not url_give:
    driver.find_element_by_name('query').send_keys(search)
    button = driver.find_element_by_xpath("//input[@type='submit']")
    button.click()

    try:
        button = driver.find_element_by_link_text('Full Story')
        button.click()
    except Exception as e:
        button = driver.find_element_by_link_text('See More Results')
        button.click()

    button = driver.find_element_by_link_text('Full Story')
    button.click()
else:
    driver.get(url_give)


comments = []

source = driver.page_source
soup = BeautifulSoup(source, 'lxml')


while page < pages:
    for i in soup.find_all('div', class_=comment_class_list):
        try:
            if page == 1:
                comment = i.find('div', class_=comment_class_page1).text
            else:
                comment = i.find('div', class_=comment_class).text
        except Exception as e:
            continue
        for z in range(len(keywords)):
            if re.search(keywords[z], comment, re.IGNORECASE):
                comments.append(comment)
            z += 1
    try:
        button = driver.find_element_by_link_text(' View more comments…')
        button.click()
        source = driver.page_source
        soup = BeautifulSoup(source, 'lxml')
        page += 1
    except NoSuchElementException:
        break

if len(comments) == 0:
    print('There are no comments available for this post')
else:
    for x in range(len(comments)):
        print(comments[x])
        print()



