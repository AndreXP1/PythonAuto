import random
import time

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

#Espera elemento carregar e clica quando possivel
def waitTimeAndClick(nav, locator, timeout = 10):
    try:
        element = WebDriverWait(nav, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element
    except Exception as e:
        #print(f"Element not found or not clickable!")
        return False

#Espera o elemento estar presente na pagina

def waitForElement(nav, locator, condition = EC.presence_of_element_located, timeout=10):
    return WebDriverWait(nav, timeout).until(condition(locator))


#Fecha popup de cookie
def close_modal(nav):
    try:
        waitTimeAndClick(nav, (By.XPATH, '//*[@class="dp-bar-button dp-bar-dismiss"]'))
        print("Modal fechado")
    except Exception as e:
        print(f"Failed to close modal: {e}")

#Procura onde esta a barra de pesquisa e pesquisa um item
def locate_search(nav):
    try:
        waitTimeAndClick(nav, (By.XPATH, '//*[@class="search-input cursor-pointer"]'))
        click_search = waitTimeAndClick(nav, (By.XPATH, '//input[@name="search"]'))
        click_search.send_keys("Câmera")
        click_search.send_keys(Keys.RETURN)
        print("Pesquisa Feita")
    except Exception as e:
        print(f"Error: {e}")


def closetab(nav):
    try:
        time.sleep(5)
        actions = ActionChains(nav)
        actions.move_by_offset(100, 50).perform()
        waitForElement(nav, (By.XPATH, '//button[@type="button" and @class="close-btn"]'))
        print("tab closed")
    except Exception as e:
        print(f"Error in closetab {e}")



def productClick(nav, scroll_pixels=200):
    try:
        time.sleep(5)
        nav.execute_script(f"window.scrollBy(0, {scroll_pixels});")
        time.sleep(2)
        try:
            element = waitForElement(nav, (By.XPATH, '//a[contains(@href, "/pt-br/camera-ip-serie-1000-com-full-color-e-ir-vip-1430-d-fc")]'))
            actions = ActionChains(nav)
            actions.move_to_element(to_element=element).perform()
            print("achou tag a")
            waitTimeAndClick(nav, (By.XPATH, '//div[contains(@class, "pb2 pl2 pr2")]'))
            return waitTimeAndClick(nav, (By.XPATH, '//a[contains(@href, "/pt-br/camera-ip-serie-1000-com-full-color-e-ir-vip-1430-d-fc")]'))
        except Exception as wait_error:
            print(f"tag a não encontrada: {wait_error}")
            return False
    except Exception as e:
        print(f"Não encontrado produto clicavel: {e}")
        return False
        

def ordemExec():
    try:
        nav = initialization()
        close_modal(nav)
        locate_search(nav)
        closetab(nav)
        productClick(nav)

        input("Press Enter to close browser...")
        nav.quit()
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    ordemExec()