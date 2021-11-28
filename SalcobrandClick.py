import random
import requests
import time
import webdriver_manager
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from bs4 import BeautifulSoup
from selenium.common.exceptions import ErrorInResponseException, NoSuchElementException

#print("comienzo")

NombreP = list()
ComponenteP = list()
PrecioP = list()
IDProducto = list()
FarmaciaP = list()

FarmaciaLocal = "Salcobrand"
def DatoNombre(ID, Nombre):
  IDProducto.append(ID)
  NombreP.append(Nombre)
  return print(f'ID: {ID} \nNombre: {Nombre}')
def DatoComponente( Componente):
  ComponenteP.append(Componente)
  return print(f'Componente: {Componente}')
def DatoPrecio(Precio, Farmacia):
  PrecioP.append(Precio)
  FarmaciaP.append(Farmacia)
  return print(f'Precio: {Precio} \nFarmacia: {Farmacia}',"\n-----------------------------------")



  #Selenium
  #driver = webdriver.Chrome('C:\\Users\\Darkoore\\Desktop\\chromedriver.exe')
driver = webdriver.Chrome('C:\\Users\\lEmma\\OneDrive\\Escritorio\\chromedriver.exe')
driver.get('https://salcobrand.cl/t/medicamentos')
wait = WebDriverWait(driver, 10)
time.sleep(5)



  #Obtencion de todos los links clickeables de los productos

contadorItems = 0
contadorWhile =0
aux= 27
try:
    
  while contadorItems <24:

      item_links = [item.get_attribute("href") for item in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".product-image > a")))] 
      #Navegador abre link
      for item_link in item_links:
        contadorItems +=1
        contadorWhile +=1
        #print(contadorItems)
        if contadorItems <=24:
          driver.get(item_link)
          try:
            Nombre = driver.find_element_by_xpath('//h2[@class="product-name"]').text
          except:
            Nombre = "Null"
            pass
          #print(f"Nombre:{Nombre}")
          DatoNombre(contadorWhile,Nombre)
          try:
            Componente = driver.find_element_by_xpath('//h3[@class="product-info"]').text.replace("Principio Activo:","")
          except:
            Componente = "Null"
            pass
          #print(f"{Componente}")
          DatoComponente(Componente)

          try:
            Precionormal = driver.find_element_by_xpath('//p[@class="normal-price"]').text.replace("Precio farmacia:","")
            DatoPrecio(Precionormal, FarmaciaLocal)
          except:
            #print("Excepcion*******************************************")
            try:
              Precionormal = driver.find_element_by_xpath('//p[@class="old"]').text.replace("Precio farmacia: ","")
              DatoPrecio(Precionormal, FarmaciaLocal)
            except:
              try:
                Precionormal = driver.find_element_by_xpath('//div[@class="normal full"]').text.replace("Total:","")
                DatoPrecio(Precionormal, FarmaciaLocal)
              except:
                try:
                  Precionormal = driver.find_element_by_css_selector('p.old').text.replace("Precio farmacia: ","")
                  DatoPrecio(Precionormal, FarmaciaLocal)
                except:
                  Precionormal = "Null"
                  DatoPrecio(Precionormal, FarmaciaLocal)
                  pass
            #print(f"{Precionormal}")
        time.sleep(random.randint(6,8))

  if contadorItems == 24:
      contadorItems=0



  #print("Comienza loop infinito")
  contadorPaginas = 2

    #Navegar a traves de cada link

  while contadorItems < 24:
      driver.get('https://salcobrand.cl/t/medicamentos')
      wait = WebDriverWait(driver, 10)
      time.sleep(5)
      #print("--------PAGINA "+str(contadorPaginas)+" ----------")

      element = driver.find_element_by_link_text(''+str(contadorPaginas)+'')
      driver.execute_script("arguments[0].click();", element)
      time.sleep(10)
      #print("AAAA")
      item_links = [item.get_attribute("href") for item in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".product-image > a")))] 
      #print("buscanding")
      for item_link in item_links:
          #Navegador abre link
          contadorItems +=1
          contadorWhile +=1
          print(contadorItems)
          if contadorItems <=24:
            driver.get(item_link)
            try:
              Nombre = driver.find_element_by_xpath('//h2[@class="product-name"]').text
            except:
              Nombre = "Null"
              pass
            #print(f"Nombre:{Nombre}")
            DatoNombre(contadorWhile,Nombre)
            try:
              Componente = driver.find_element_by_xpath('//h3[@class="product-info"]').text.replace("Principio Activo:","")
            except:
              Componente = "Null"
              pass
            #print(f"{Componente}")
            DatoComponente(Componente)

            try:
              Precionormal = driver.find_element_by_xpath('//p[@class="normal-price"]').text.replace("Precio farmacia:","")
              DatoPrecio(Precionormal, FarmaciaLocal)
            except:
              #print("Excepcion*******************************************")
              try:
                Precionormal = driver.find_element_by_xpath('//p[@class="old"]').text.replace("Precio farmacia: ","")
                DatoPrecio(Precionormal, FarmaciaLocal)
              except:
                try:
                  Precionormal = driver.find_element_by_xpath('//div[@class="normal full"]').text.replace("Total:","")
                  DatoPrecio(Precionormal, FarmaciaLocal)
                except:
                  try:
                    Precionormal = driver.find_element_by_css_selector('p.old').text.replace("Precio farmacia: ","")
                    DatoPrecio(Precionormal, FarmaciaLocal)
                  except:
                    Precionormal = "Null"
                    DatoPrecio(Precionormal, FarmaciaLocal)
                    pass
              #print(f"{Precionormal}")

          if(contadorItems==24):
            #print("-----------------------------*Reset")
            contadorItems=0
            contadorPaginas+=1
          time.sleep(random.randint(6,8))
except:
  print("********** Pagina 5 alcanzada....")
pass

contadorItems=0
Pagina5 =5
try:
  while contadorItems < 24:
      driver.get('https://salcobrand.cl/t/medicamentos')
      wait = WebDriverWait(driver, 10)
      time.sleep(5)
      #print("--------PAGINA "+str(contadorPaginas)+" ----------")
      element = driver.find_element_by_link_text(''+str(Pagina5)+'')
      driver.execute_script("arguments[0].click();", element)
      time.sleep(5)
      element = driver.find_element_by_link_text(''+str(contadorPaginas)+'')
      driver.execute_script("arguments[0].click();", element)
      time.sleep(10)
      #print("AAAA")
      item_links = [item.get_attribute("href") for item in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".product-image > a")))] 
      #print("buscanding")
      for item_link in item_links:
          #Navegador abre link
          contadorItems +=1
          contadorWhile +=1
          print(contadorItems)
          if contadorItems <=24:
            driver.get(item_link)
            try:
              Nombre = driver.find_element_by_xpath('//h2[@class="product-name"]').text
            except:
              Nombre = "Null"
              pass
            #print(f"Nombre:{Nombre}")
            DatoNombre(contadorWhile,Nombre)
            try:
              Componente = driver.find_element_by_xpath('//h3[@class="product-info"]').text.replace("Principio Activo:","")
            except:
              Componente = "Null"
              pass
            #print(f"{Componente}")
            DatoComponente(Componente)

            try:
              Precionormal = driver.find_element_by_xpath('//p[@class="normal-price"]').text.replace("Precio farmacia:","")
              DatoPrecio(Precionormal, FarmaciaLocal)
            except:
              #print("Excepcion*******************************************")
              try:
                Precionormal = driver.find_element_by_xpath('//p[@class="old"]').text.replace("Precio farmacia: ","")
                DatoPrecio(Precionormal, FarmaciaLocal)
              except:
                try:
                  Precionormal = driver.find_element_by_xpath('//div[@class="normal full"]').text.replace("Total:","")
                  DatoPrecio(Precionormal, FarmaciaLocal)
                except:
                  try:
                    Precionormal = driver.find_element_by_css_selector('p.old').text.replace("Precio farmacia: ","")
                    DatoPrecio(Precionormal, FarmaciaLocal)
                  except:
                    Precionormal = "Null"
                    DatoPrecio(Precionormal, FarmaciaLocal)
                    pass
              #print(f"{Precionormal}")

          if(contadorItems==24):
            #print("-----------------------------*Reset")
            contadorItems=0
            contadorPaginas+=1
          time.sleep(random.randint(6,8))
except:
  print("Datos listoss")
pass

df = pd.DataFrame({'ID': IDProducto, 'Nombre':NombreP, 'Componente': ComponenteP, 'Precio': PrecioP, 'Farmacia': FarmaciaP}, index=list(range(1,contadorWhile+1)))
print(df)
df.to_csv('Salcobrand_WS.csv', index=False)
columns = ['ID', 'Nombre', 'Componente', 'Precio']
df = pd.read_csv('Salcobrand_WS.csv', names=columns)

print("Término de código")


