import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import os


@pytest.fixture
def driver_init():
    # Create driver for Chrome
    driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
    service = Service(driver_path)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging', ])

    driver = webdriver.Chrome(
        options=options,
        service=service
    )
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.close()


def auth_user(username, password, driver):
    # Login #
    input_username = wait_of_element_located(xpath='//*[@id="user-name"]', driver=driver)
    input_password = wait_of_element_located(xpath='//*[@id="password"]', driver=driver)
    login_button = wait_of_element_located(xpath='//*[@id="login-button"]', driver=driver)

    input_username.send_keys(username)
    input_password.send_keys(password)
    login_button.send_keys(Keys.RETURN)
    # #


def wait_of_element_located(xpath, driver):
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return element


def test_site(driver_init):

    auth_user('standard_user', 'secret_sauce', driver=driver_init)
    # Find item #
    item = wait_of_element_located(xpath='//*[@id="item_5_title_link"]/div', driver=driver_init)
    item.click()
    # Add to cart #
    add_to_cart = wait_of_element_located(
        xpath='//*[@id="add-to-cart-sauce-labs-fleece-jacket"]',
        driver=driver_init
    )
    add_to_cart.click()
    # Cart #
    cart = wait_of_element_located(xpath='//*[@id="shopping_cart_container"]/a', driver=driver_init)
    cart.click()
    # Cart items #
    cart_item = wait_of_element_located(xpath='//*[@id="item_5_title_link"]/div', driver=driver_init)
    cart_desc = wait_of_element_located(
        xpath='//*[@id="cart_contents_container"]/div/div[1]/div[3]/div[2]/div[1]',
        driver=driver_init
        )
    print(cart_item.text)
    print(cart_desc.text)

    assert cart_item.text == "Sauce Labs Fleece Jacket"
    assert cart_desc.text == "It's not every day that you come across a midweight quarter-zip fleece jacket " \
                             "capable of handling everything from a relaxing day outdoors to a busy day at the office."


if __name__ == '__main__':
    test_site()
