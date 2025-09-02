import os
import time
import test_selenium
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
 
#Espera carregamento da pagina.
def wait_last_page(nav):
    try:
        nav.save_screenshot("prints/PageItem.png")
        test_selenium.wait_for_element(nav, (By.XPATH, '//*[@class="page-product"]'))

        #Captura body elements dentro da pagina
        soup = BeautifulSoup(nav.page_source, 'html.parser')
        body_tag = soup.body
        #Retorna body em formato de string
        if body_tag:
            return str(body_tag)
        else:
            print("No body tag found")
            return ""
    except Exception as e:
        print(f"Error during page loading: {e}")


#Função que adiciona o body pego pelo scraping dentro de outro arquivo
def insert_body_into_html(body_content, src_path="default.html", dst_path="tests/default.html"):

#Cria diretório "/tests" se anida não existir
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
