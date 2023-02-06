from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r'user-data-dir=' + dir_path + "profile/zap")
driver = webdriver.Chrome(chrome_options=chrome_options2)
driver.get('https://web.whatsapp.com/')
time.sleep(120)
