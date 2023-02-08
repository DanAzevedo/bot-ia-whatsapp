from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import openai
import time
import os

# Salvar a sessão retirando a necessidade de leitura do QR Code novamente
dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r'user-data-dir=' + dir_path + "profile/zap")
driver = webdriver.Chrome(options=chrome_options2)
driver.get('https://web.whatsapp.com/')

##########################################API DO EDITACODIGO##########################################
# Caso o WhatsApp mude o nome da classe, essa API ajuda atualizando sozinho o nome da classe
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/59.0.3071.115 Safari/537.36'}

api = requests.get("https://editacodigo.com.br/index/api-whatsapp/z1A1JRIvFqrKQN0YeLSca8kdDWIPhFV4", headers=agent)
time.sleep(1)
api = api.text
api = api.split(".n.")
bolinha_notificacao = api[3].strip()
contato_cliente = api[4].strip()
caixa_msg = api[5].strip()
msg_cliente = api[6].strip()
######################################################################################################
time.sleep(15)


def bot():
    try:
        # 1 - PEGAR A MENSAGEM E CLICAR NELA
        # Para buscar uma notificação
        notif_tag = driver.find_element(By.CLASS_NAME, bolinha_notificacao)
        # Para buscar várias notificações
        notif_tag = driver.find_elements(By.CLASS_NAME, bolinha_notificacao)
        # Buscar a mais recente indicando -1 no índice
        notif_click = notif_tag[-1]
        # Click na tag verde de notificação de mensagem não lida
        action_notif = webdriver.common.action_chains.ActionChains(driver)
        # Movendo o mouse para a posição em que o elemento irá se deslocar
        action_notif.move_to_element_with_offset(notif_click, 0, -20)
        # Click duplo
        action_notif.click()
        action_notif.perform()
        action_notif.click()
        action_notif.perform()

        # 2 - LER A NOVA MENSAGEM
        all_msg = driver.find_elements(By.CLASS_NAME, msg_cliente)
        # Fazendo uma lista e transformando em texto todas as mensagens que chegaram
        all_msg_txt = [e.text for e in all_msg]
        # Pegando somente a última mensagem
        msg = all_msg_txt[-1]
        print(msg)

        # 3 - PROCESSA A MENSAGEM NA API IA
        ##########################################API DO OPENAI##########################################
        openai.api_key = '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'

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=msg,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ret = response['choices'][0]['text']
        print(ret)
        time.sleep(3)
        ################################################################################################

        # 4 - RESPONDE A MENSAGEM
        # Seleciona a caixa de mensagem e clica
        text_field = driver.find_element(By.XPATH, caixa_msg)
        text_field.click()
        time.sleep(3)
        text_field.send_keys(ret, Keys.ENTER)
        time.sleep(2)

        # 5 - FECHA O CONTATO
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except:
        print('Buscando novas notificações...')
        time.sleep(3)


while True:
    bot()
