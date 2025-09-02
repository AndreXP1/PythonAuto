import os
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
from html_utils import wait_last_page as wp, insert_body_into_html as ib


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

#Espera o elemento estar presente na pagina

def wait_for_element(nav, locator, condition = EC.presence_of_element_located, timeout=10):
    return WebDriverWait(nav, timeout).until(condition(locator))


#Função que desce a pagina kk
def page_scroll(driver, scroll_pixels, timeout):
    time.sleep(timeout)
    driver.execute_script(f"window.scrollBy(0, {scroll_pixels});")

#Fecha popup de cookie
def close_modal(nav):
    try:
        wait_time_and_click(nav, (By.XPATH, '//*[@class="dp-bar-button dp-bar-dismiss"]'))
        print("Modal Closed")
    except Exception as e:
        print(f"Failed to close modal: {e}")

#Procura onde esta a barra de pesquisa e pesquisa um item
def locate_search(nav):
    try:
        wait_time_and_click(nav, (By.XPATH, '//*[@class="search-input cursor-pointer"]'))
        click_search = wait_time_and_click(nav, (By.XPATH, '//input[@name="search"]'))
        click_search.send_keys("Câmera")
        nav.save_screenshot("prints/Search.png")
        click_search.send_keys(Keys.RETURN)
        print("Search Done")
        
    except Exception as e:
        print(f"Error: {e}")

#Fecha dropdown de contato (mexe o mouse um pouco pra atualizar a pagina, não sei por que que é assim)
def close_tab(nav):
    try:
        time.sleep(1)
        actions = ActionChains(nav)
        actions.move_by_offset(100, 50).perform()
        print("Tab Closed")
    except Exception as e:
        print(f"Error in closetab {e}")


#Desce pagina em 200 pixels e clica no produto do link (talvez desenvolver funcao para qualquer um dos itens presentes ao inves de um especifico...)
def product_click(nav):
    try:
        page_scroll(nav, 200, 2)
        try:
            nav.save_screenshot("prints/Item.png")
            #Aberração criada abaixo.
            #Procura numero de items dentro de "divs" e depois procura o numero de links dentro de "items" e tenta clicar em qualquer um.
            divs = nav.find_elements(By.XPATH, '//div[@class="block-dynamic-list small product-dynamic-list"]')
            for div in divs:
                items = div.find_elements(By.XPATH, './/div[@class="pb2 pl2 pr2"]')
                for item in items:
                    links = item.find_elements(By.TAG_NAME, 'a')
                    for link in links:
                        try:
                            link.click()
                            print("Product Clicked")
                            return True
                        except Exception as e:
                            print(f"Error while trying to click product {e}")
        except Exception as wait_error:
            print(f"Wait_Error: {wait_error}")
            return False
    except Exception as e:
        print(f"Unable to scroll: {e}")
        return False

#Ordem de execução do programa
def ordem_exec():
    try:
        nav = initialization()
        close_modal(nav)
        locate_search(nav)
        close_tab(nav)
        product_click(nav)
        body_str = wp(nav)
        ib(body_str)

        input("Press Enter to close browser...")
        nav.quit()
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    ordem_exec()