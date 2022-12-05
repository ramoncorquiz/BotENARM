#LIBRERIA PARA HACER INPUT Y LEER DATOS DE UNA PAGINA WEB
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support  import expected_conditions as EC

#LIBRERIA PARA ENVIAR MENSAJES DE WHATSAPP
import pywhatkit
#LIBRERIA PARA HACER DELAY DE TIEMPOº
import time

#Importa las requests para 2captcha
import requests


browser = webdriver.Edge()

browser.get('https://enarm.salud.gob.mx/enarm/2022/especialidad/seleccionEnarm')

assert 'ENARM' in browser.title


browser.find_element(By.CLASS_NAME, "btn-secondary").click()

time.sleep(2)

elem = browser.find_element(By.ID, "user")
elem.send_keys('GUMP980127MBCTRL09')

elem2 = browser.find_element(By.ID, "folio")
elem2.send_keys('28319')

elem3 = browser.find_element(By.ID,"password")
elem3.send_keys('19982701p')
time.sleep(3)


site_key = "6Ldn90UhAAAAAJiqTLRCdtp3lzS-eA755SwWoI89"
page_url = "https://enarm.salud.gob.mx/enarm/2022/especialidad/"
method = "userrecaptcha"
key = "fb9b5caf2e3a50f257310bdb3c7ee078"

url = "http://2captcha.com/in.php?key={}&method={}&googlekey={}&pageurl={}".format(key,method,site_key,page_url)
response = requests.get(url)

if response.text[0:2] != 'OK':
    quit('Service error. Error code:' + response.text)
captcha_id = response.text[3:]

print("El codigo es " + captcha_id)
token_url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(key,captcha_id)

while True:
    time.sleep(10)
    response = requests.get(token_url)

    if response.text[0:2] == 'OK':
        break

captcha_results = response.text[3:]

elementoCaptcha = browser.find_element(By.ID, "g-recaptcha-response")
display_prop = elementoCaptcha.value_of_css_property('display')
if display_prop == 'none':
    browser.execute_script("arguments[0].style.display = 'block'", elementoCaptcha)

browser.execute_script("""document.querySelector('[name="g-recaptcha-response"]').innerText='{}'""".format(captcha_results))
browser.find_element(By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']").click()


time.sleep(5)
elem3.send_keys(Keys.ENTER)

time.sleep(5)


valorMed = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[15]/div/p/small[2]").text
print(valorMed)

mensajeWhatsApp= valorMed + " plazas de medicina familiar"
pywhatkit.sendwhatmsg_instantly("+526462188266", mensajeWhatsApp, 10)


  



