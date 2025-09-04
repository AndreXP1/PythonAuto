import random
import time
from html_utils import insert_body_into_html as ib
from html_utils import wait_last_page as wp
from html_utils import change_styles as cs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())


def initialization():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    nav = webdriver.Chrome(service=service, options=options)
    nav.get("https://intelbras.com.br")
    time.sleep(random.uniform (1, 3))
    return nav


#Waits for element to load and clicks when possible
def wait_time_and_click(nav, locator, timeout = 10):
    try:
        element = WebDriverWait(nav, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element
    except Exception as e:
        print(f"Element not found or not clickable!")
        return print(f"Error {e}")
    

#Waits for the element to be present on the page
def wait_for_element(nav, locator, condition = EC.presence_of_element_located, timeout=10):
    return WebDriverWait(nav, timeout).until(condition(locator))


#Function that scrolls down the page
def page_scroll(driver, scroll_pixels, timeout):
    time.sleep(timeout)
    driver.execute_script(f"window.scrollBy(0, {scroll_pixels});")


#Closes cookie popup
def close_modal(nav):
    try:
        wait_time_and_click(nav, (By.XPATH, '//*[@class="dp-bar-button dp-bar-dismiss"]'))
        print("Modal Closed")
    except Exception as e:
        print(f"Failed to close modal: {e}")


#Finds where the search bar is and searches for an item
def locate_search(nav):
    try:
        wait_time_and_click(nav, (By.XPATH, '//*[@class="search-input cursor-pointer"]'))
        click_search = wait_time_and_click(nav, (By.XPATH, '//input[@name="search"]'))
        click_search.send_keys("Câmera")
        save_print(nav)
        click_search.send_keys(Keys.RETURN)
        print("Search Done")
        
    except Exception as e:
        print(f"Error: {e}")


#Closes contact dropdown (moves the mouse a bit to refresh the page, not sure why this is needed)
def close_tab(nav):
    try:
        time.sleep(1)
        actions = ActionChains(nav)
        actions.move_by_offset(100, 50).perform()
        print("Tab Closed")
    except Exception as e:
        print(f"Error in closetab {e}")


#Find target Div and look for other target divs inside.
def search_into_div(nav):
    try:
        divs = nav.find_elements(By.XPATH, '//div[@class="block-dynamic-list small product-dynamic-list"]')
        for div in divs:
                items = div.find_elements(By.XPATH, './/div[@class="pb2 pl2 pr2"]')
        return items
    except Exception as e:
        print(f"Unable to find Div {e}")


#Find tag items inside the target divs from search_into_div function
def find_item(nav):
    try:
        items = search_into_div(nav)
        links = []
        for item in items:
            links.extend(item.find_elements(By.TAG_NAME, 'a'))
        return links
    except Exception as e:
        print(f"Unable to find item due to: {e}")


#Scroll down until element is visible, waits 1 second and then clicks on the first element found in find_item function
def click_link(nav):
    try:
        page_scroll(nav, 200, 2)
        time.sleep(1)
        links = find_item(nav)
        for link in links:
            try:
                link.click()
                print("Product Clicked")
                save_print(nav)
                return True
            except Exception as e:
                print(f"Error while trying to click product: {e}")
    except Exception as e:
        print(f"Error: {e}")


def save_print(nav):
    try:
        nav.save_screenshot("prints/Item.png")
    except Exception as e:
        print(f"Something went wrong: {e}")


#Order of program execution
def ordem_exec():
    try:
        nav = initialization()
        close_modal(nav)
        locate_search(nav)
        close_tab(nav)
        search_into_div(nav)
        find_item(nav)
        click_link(nav)
        save_print(nav)
        body_str = wp(nav)
        ib(body_str)
        # cs(nav)

        input("Press Enter to close browser...")
        nav.quit()
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    ordem_exec()