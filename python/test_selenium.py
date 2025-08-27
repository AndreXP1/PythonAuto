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
            wait_time_and_click(nav, (By.XPATH, '//a[contains(@href, "/pt-br/camera-ip-serie-1000-com-full-color-e-ir-vip-1430-d-fc")]'))
            print("Product Clicked")
        except Exception as wait_error:
            print(f"tag not found: {wait_error}")
            return False
    except Exception as e:
        print(f"Unable to scroll: {e}")
        return False



def wait_last_page(nav):
    try:
        wait_for_element(nav, (By.XPATH, '//*[@class="page-product"]'))
        
        soup = BeautifulSoup(nav.page_source, 'html.parser')
        
        # Cria um diretório para salvar os arquivos CSS
        css_dir = "css_files"
        if not os.path.exists(css_dir):
            os.makedirs(css_dir)

        # Encontra todas as tags <link> de CSS
        css_links = soup.find_all('link', rel='stylesheet')
        
        for index, link in enumerate(css_links):
            href = link.get('href')
            if href:
                # Constrói a URL completa do arquivo CSS
                css_url = urljoin(nav.current_url, href)
                try:
                    # Baixa o conteúdo do CSS
                    response = requests.get(css_url)
                    response.raise_for_status()
                    
                    # Salva o conteúdo em um arquivo .css
                    file_name = f"style_{index}.css"
                    local_path = os.path.join(css_dir, file_name)
                    with open(local_path, "w", encoding="utf-8") as css_file:
                        css_file.write(response.text)
                    print(f"CSS salvo em {local_path}")
                    
                    # Atualiza o href no HTML para o caminho local
                    link['href'] = local_path

                except requests.exceptions.RequestException as e:
                    print(f"Erro ao baixar {css_url}: {e}")

        # Salva o HTML MODIFICADO no arquivo de saída
        with open("output.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
        print("Página completa e CSS localmente linkado salvos em output.html")

    except Exception as e:
        print(f"Erro ao processar a página do produto: {e}")




#Ordem de execução do programa
def ordem_exec():
    try:
        nav = initialization()
        close_modal(nav)
        locate_search(nav)
        close_tab(nav)
        product_click(nav)
        wait_last_page(nav)

        input("Press Enter to close browser...")
        nav.quit()
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    ordem_exec()