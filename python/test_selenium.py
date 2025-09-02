import os
import random
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
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

#Fecha dropdown de contato (mexe o mouse um pouco pra atualizar a pagina, não sei por que q é assim)
def close_tab(nav):
    try:
        time.sleep(1)
        actions = ActionChains(nav)
        actions.move_by_offset(100, 50).perform()
        print("Tab closed")
    except Exception as e:
        print(f"Error in closetab {e}")


#Desce pagina em 200 pixels e clica no produto do link (talvez desenvolver funcao para qualquer um dos itens presentes ao inves de um especifico...)
def product_click(nav):
    try:
        page_scroll(nav, 200, 2)
        try:
            nav.save_screenshot("prints/Item.png")
            #Aberração criada abaixo.
            #Procura numero de items dentro de "divs" e depois procura o numero de links dentro de "items" e clica no primeiro.
            divs = nav.find_elements(By.XPATH, '//div[@class="block-dynamic-list small product-dynamic-list"]')
            for div in divs:
                items = div.find_elements(By.XPATH, './/div[@class="pb2 pl2 pr2"]')
                for item in items:
                    links = item.find_elements(By.TAG_NAME, 'a')
                    for link in links:
                        try:
                            link.click()
                            print("product clicked")
                            break
                        except Exception as e:
                            print(f"did not click {e}")
        except Exception as wait_error:
            print(f"Wait_Error: {wait_error}")
            return False
    except Exception as e:
        print(f"Unable to scroll: {e}")
        return False


#espera carregamento da pagina.
def wait_last_page(nav):
    try:
        nav.save_screenshot("prints/PageItem.png")
        wait_for_element(nav, (By.XPATH, '//*[@class="page-product"]'))

        #Captura body elements dentro da pagina
        soup = BeautifulSoup(nav.page_source, 'html.parser')
        body_tag = soup.body
        if body_tag:
            return str(body_tag)
        else:
            print("No body tag found")
            return ""
    except Exception as e:
        print(f"Erro ao processar a página do produto: {e}")

#Função que adiciona o body pego pelo scraping dentro de outro arquivo
def insert_body_into_html(body_content, src_path="default.html", dst_path="tests/default.html"):
    from bs4 import BeautifulSoup
    import os

    
    dst_dir = os.path.dirname(dst_path)
    if dst_dir and not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

#Le arquivo original
    with open(src_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

#Se tiver tag body no arquivo orignal remove ela
    if soup.body:
        soup.body.decompose()

#Cria nova tag body e insere o conteudo nela.
    new_body = soup.new_tag("body")
    new_body.append(BeautifulSoup(body_content, "html.parser"))
    soup.html.append(new_body)

#Passa o body para o outro arquivo
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Body content inserted into {dst_path}")


#Ordem de execução do programa
def ordem_exec():
    try:
        nav = initialization()
        close_modal(nav)
        locate_search(nav)
        close_tab(nav)
        product_click(nav)
        body_str = wait_last_page(nav)
        insert_body_into_html(body_str)

        input("Press Enter to close browser...")
        nav.quit()
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    ordem_exec()