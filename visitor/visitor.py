import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import visitor.pages as pages
from random import randint

standard_wait_time = 15
def wait_and_return(driver, xpath, time_in_sec):
    wait = WebDriverWait(driver, time_in_sec)
    element = wait.until( \
        EC.element_to_be_clickable( \
            (By.XPATH, xpath)))
    return element

def find_by_xpath(driver, xpath):
    return driver.find_element(By.XPATH, xpath)

def find_multiple_by_xpath(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)

def random_index_generator(list):
    return randint(0, len(list)-1)

def fill_input(element, text):
    element.clear()
    element.send_keys(text)

def visitor_emulate(chromedriver):
    try:
        driver = chromedriver
        # Navigating to the below pages randomly
        page_list = pages.pages()
        random_page = page_list[random_index_generator(page_list)]
        print('Visiting the random page: ' + random_page['context'])
        driver.get(random_page['url'])
        # City chooser button: Delhi, Gurgaon and NCR
        city_chooser = wait_and_return( \
            driver, \
            '/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div/div/button', \
            10)
        print('City delhi chosen successfully')
        city_chooser.click()
        wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div/div[4]/section/div/div[1]', standard_wait_time)
        random_products_card_xpath = '//*[@id="app"]/div/div/div[2]/div/div/div[4]/section/div/div'
        random_products = find_multiple_by_xpath(driver, random_products_card_xpath)
        # Click on a random_product
        random_products[random_index_generator(random_products)].click()
        print('Chose a random product successfully')
        buy_now_button = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div/div[2]/div/div[3]/div/div[1]/div[5]/button', standard_wait_time)
        print('The product page loaded is: ' + driver.title)
        buy_now_button.click()
        print('Clicked on buy now')
        proceed_to_next = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/button', standard_wait_time)
        print('Clicked on proceed to next')
        proceed_to_next.click()
        # Now start filling the address form
        name_field = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/form/div[1]/div/input', standard_wait_time)
        phone_field = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/form/div[2]/div/input', standard_wait_time)
        email_field = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/form/div[3]/div/input', standard_wait_time)
        pincode_field = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/form/div[4]/div/input', standard_wait_time)
        address_field = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/form/div[5]/div/textarea', standard_wait_time)
        fill_input(name_field, 'Chrome Automation')
        fill_input(phone_field, '7596779999')
        fill_input(email_field, 'chrome_automation@gozefo.com')
        fill_input(pincode_field, '560078')
        fill_input(address_field, 'This is a fake order being places by chrome automation. Please contanct ghazi@gozefo.com for details')
        print('Filled the form inputs successfully')
        choose_payment = wait_and_return(driver, '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/form/div[7]/div/div/button', standard_wait_time)
        choose_payment.click()
        wait_and_return(driver, '//*[@id="react-tabs-19"]/div/div/div/div/button', standard_wait_time)
        print('On page place order. Sleeping for 2 minutes and exiting')
        time.sleep(2)
    except Exception as err:
        print(err)