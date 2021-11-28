from bs4 import BeautifulSoup
import requests
from time import *
from random import randint


azar = randint(2,5)
Pagina=0


Link = requests.get('https://www.cruzverde.cl/medicamentos/?start=0&sz=18&maxsize=18')
soup = BeautifulSoup(Link.content, 'lxml')
tabla = soup.find_all('div', class_ = 'tile-body px-3 pt-3 pb-0 d-flex flex-column pb-0')
#print(tabla)

for datos in tabla:
        Nombre = datos.find('a', class_ = 'link').text.replace(' ','')
        Marcas = datos.find('a', class_ = 'product-brand text-uppercase m-0').text.replace(' ','')
        PrecioOferta = datos.find('span', class_ = 'value').text.replace('(Oferta)','')
        PrecioNormal = datos.find('span', class_ = 'price-original').text.replace('(Normal)','')



        print(f" Nombre producto:{Nombre.strip()}") 
        print(f" Marcas:{Marcas.strip()}") 
        print(f" Precio :{PrecioNormal.strip()}") 
        print(f" Precio Oferta:{PrecioOferta.strip()}") 
        print(f" ")
        print(f" ")
        print(f" ")
#Pagina=Pagina+18
#print (Pagina)
        #sleep(azar)
        

