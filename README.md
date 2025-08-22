# PythonAuto

PythonAuto

Este projeto automatiza a navegação e interação com o site da Intelbras utilizando Selenium WebDriver em Python. O objetivo é simular ações de um usuário, como fechar pop-ups, pesquisar produtos, interagir com elementos da página e extrair informações específicas.

## Contextualização

O código principal está em `python/test_selenium.py` e realiza as seguintes etapas:

1. **Inicialização do navegador**: Configura o Chrome para automação, desabilitando algumas detecções de automação e maximizando a janela.
2. **Fechamento de pop-up de cookies**: Localiza e fecha o modal de cookies ao acessar o site.
3. **Pesquisa de produto**: Interage com a barra de pesquisa para buscar por "Câmera".
4. **Interação com elementos**: Move o mouse para fechar dropdowns e clica em um produto específico após rolar a página.
5. **Extração de dados**: Após acessar a página do produto, utiliza BeautifulSoup para extrair o nome do produto e salva o resultado em `output.html`.
6. **Encerramento**: Aguarda interação do usuário para fechar o navegador.

## Requisitos

- Python 3.13+
- Selenium
- webdriver-manager
- beautifulsoup4

Instale as dependências com:

```bash
pip install selenium webdriver-manager beautifulsoup4
```

## Execução

Execute o script principal:

```bash
python python/test_selenium.py
```

## Estrutura

- `python/test_selenium.py`: Script principal de automação.
- `python/output.html`: Arquivo gerado com o resultado da extração.

## Observações

- O script foi desenvolvido para fins de aprendizado e demonstração de automação web.
- Certifique-se de que o Chrome está instalado e atualizado.
- O código pode ser adaptado para outros sites ou produtos conforme necessário.
