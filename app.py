from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

app = Flask(__name__)

# Configuração do Selenium e ChromeDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Rodar o Chrome em modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    servico = Service(os.getenv('CHROMEDRIVER_PATH', '/usr/bin/chromedriver'))
    driver = webdriver.Chrome(service=servico, options=chrome_options)
    return driver

# Função para acessar o site e capturar o resultado
@app.route('/api/execute-site-task', methods=['POST'])
def execute_task():
    data = request.json
    url = data.get('url')
    input_field_selector = data.get('input_selector')
    submit_button_selector = data.get('submit_selector')
    result_selector = data.get('result_selector')
    input_value = data.get('input_value')
    
    driver = setup_driver()
    driver.get(url)
    
    # Preencher o campo e submeter o formulário
    input_element = driver.find_element(By.CSS_SELECTOR, input_field_selector)
    input_element.send_keys(input_value)
    submit_button = driver.find_element(By.CSS_SELECTOR, submit_button_selector)
    submit_button.click()
    
    # Aguarde o resultado
    time.sleep(5)  # Ajuste o tempo de espera conforme necessário
    
    result_element = driver.find_element(By.CSS_SELECTOR, result_selector)
    result_text = result_element.text
    
    driver.quit()
    
    response = {
        "status": "success",
        "result": result_text
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
