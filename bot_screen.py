from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import openai
import logging
import PySimpleGUI as sg

logger = logging.getLogger(__name__)

# #########################################API DO EDITACODIGO##########################################
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/59.0.3071.115 Safari/537.36'}

api = requests.get("https://editacodigo.com.br/index/api-whatsapp/z1A1JRIvFqrKQN0YeLSca8kdDWIPhFV4", headers=agent)
time.sleep(1)
api = api.text
api = api.split(".n.")
token1 = api[0].strip()
token2 = api[1].strip()
token3 = api[2].strip()
bolinha_notificacao = api[3].strip()
contato_cliente = api[4].strip()
caixa_msg = api[5].strip()
msg_cliente = api[6].strip()


# #####################################################################################################

# #########################################BOT#########################################################
def bot():
    try:
        # 1 - PEGAR A MENSAGEM E CLICAR NELA
        # Para buscar uma notificação
        # notif_tag = driver.find_element(By.CLASS_NAME, bolinha_notificacao)
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

        client = 'mensagem do cliente:'
        text2 = 'Responda a mensagem do cliente com base no proximo texto'
        # texto = 'explique que você é uma inteligência artificial e a ausência com o motivo de que Daniel está ' \
        #       'programando ou estudando e pça que deixa uma mensagem adiantando o assunto e se tem alguma urgência.'
        question = client + msg + text2 + texto

        # 3 - PROCESSA A MENSAGEM NA API IA
        # #########################################API DO OPENAI##########################################
        openai.api_key = apiopenai.strip()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ret = response['choices'][0]['text']
        print(ret)
        time.sleep(3)
        # ###############################################################################################

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
        logger.error(print('Buscando novas notificações...'))
        time.sleep(3)
        raise


# #####################################################################################################

# ####################TELAS#####################
img = sg.Image(filename='ia.png', key='-IMAGE-')
img2 = sg.Image(filename='ia.png', key='_CAMIMAGE_')

screen1 = [
    [sg.Column([[img]], justification='center')],
    [sg.Text('PASS')],
    [sg.Input(key='pass')],
    [sg.Button('LOGIN')],
    [sg.Text('', key='error')]
]

screen2 = [
    [sg.Column([[img2]], justification='center')],
    [sg.Text('BEM VINDO AO BOT DE INTELIGÊNCIA ARTIFICIAL')],
    [sg.Text('Insira sua key da OpenAI')],
    [sg.Input(key='apiopenai')],
    [sg.Multiline(size=(80, 20), key='texto')],
    [sg.Text('TENHA O CELULAR EM MÃOS')],
    [sg.Text('CLIQUE ABAIXO PARA CAPTURAR O QR CODE')],
    [sg.Button('CAPTURAR QRCODE')],
]
# ###########################################

windows1 = sg.Window('IA BOT', layout=screen1)
windows2 = sg.Window('IA BOT', layout=screen2)

while True:
    event, values = windows1.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'LOGIN':
        password = values['pass']
        if password == token1 or password == token2 or password == token3:
            windows1.close()
            event2, values2 = windows2.read()
            if event2 == 'CAPTURAR QRCODE':
                apiopenai = values2['apiopenai']
                texto = values2['texto']
                windows2.close()
                dir_path = os.getcwd()
                chrome_options2 = Options()
                chrome_options2.add_argument(r"user-data-dir=" + dir_path + "profile/zap")
                driver = webdriver.Chrome(options=chrome_options2)
                driver.get('https://web.whatsapp.com/')
                time.sleep(10)
                while True:
                    bot()

            if event2 == sg.WIN_CLOSED:
                break
        else:
            screen1["error"].update('Senha incorreta!')
