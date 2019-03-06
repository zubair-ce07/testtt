import time
from selenium import webdriver


def main():

    driver = webdriver.Chrome()
    driver.get("https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f")
    email = driver.find_element_by_css_selector("input#email")
    email.click()
    email.send_keys("shahrukhijaz31@gmail.com")
    password = driver.find_element_by_css_selector("input#password")
    password.click()
    password.send_keys("shahrukh31")
    login = driver.find_element_by_css_selector("button#submit-button")
    login.click()
    time.sleep(3)
    ask_question = driver.find_element_by_css_selector('div[aria-label="ask new question"]')
    ask_question.click()

    title = driver.find_element_by_css_selector("input#title")
    title.click()
    title.send_keys("How to use OR operator in css-selector in python ?")
    time.sleep(2)
    body = driver.find_element_by_css_selector("textarea#wmd-input")
    body.click()
    body.send_keys("I am new to selenium , I want to use OR operator between css-selector \n"
                   "I am trying using || operator "
                   "but it did not work for me. I am trying to do something like this:\n \n"
                   "driver.find_element_by_css_selector(div[(id='resultVersionA']||[id='resultVersionB')])")
    time.sleep(3)
    nextstep = driver.find_element_by_css_selector("input#tageditor-replacing-tagnames--input")
    nextstep.click()
    nextstep.send_keys("selenium-webdriver css-selectors python ")
    time.sleep(3)
    post = driver.find_element_by_css_selector("button#submit-button")
    post.click()
    time.sleep(3)
    form = driver.find_element_by_css_selector('a[title="A list of all 174 Stack Exchange sites"]')
    form.click()
    time.sleep(3)
    logout = driver.find_element_by_partial_link_text("log out")
    logout.click()
    time.sleep(3)
    logout = driver.find_element_by_css_selector('input[value="Log Out"]')
    logout.click()
    time.sleep(10)
    driver.close()


if __name__ == "__main__":
    main()
