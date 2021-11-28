from os import link
from bs4 import BeautifulSoup
from urllib.request import urlopen
from time import *
from datetime import datetime
import datetime
import datetime
import ssl
import pandas as pd
import re
import csv
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false, null
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey, MetaData
from sqlalchemy.sql.sqltypes import Date
import matplotlib.pyplot as plt
import os

# pyodbc stuff for MS SQL Server Express
driver='{ODBC Driver 17 for SQL Server}'
server='LAPTOP-PL59D9FT\SQLEXPRESS'
database='Equifarmace'
trusted_connection='yes'

# pyodbc connection string
connection_string = f'DRIVER={driver};SERVER={server};'
connection_string += f'DATABASE={database};'
connection_string += f'TRUSTED_CONNECTION={trusted_connection}'

# create sqlalchemy engine connection URL
connection_url = URL.create(
    "mssql+pyodbc", query={"odbc_connect": connection_string})


engine = create_engine(connection_url)

now = datetime.datetime.now()
fecha = (str(now.year)+"/"+str(now.month)+"/"+str(now.day))
# 2015 5 6 8 53 40
meta_data=MetaData()
productos = Table('producto', meta_data,
    Column('idProducto', Integer, autoincrement=False, primary_key=True),
    Column('nombre', String, nullable=False),
    Column('componente', String, nullable=False),
)

detalleProducto = Table('detalleProducto', meta_data,
    Column('idDetalle', Integer, autoincrement=False, primary_key=True),
    Column('precio', Float, nullable=False),
    Column('fecha', Date(),  nullable=False),
    Column('farmacia', String),
    Column('link', String),
    Column('idProducto', Integer, ForeignKey("producto.idProducto"), nullable=False),
)

engine = create_engine(connection_url)
Base= declarative_base()
Base2= declarative_base()
class Productos(Base):
    __tablename__="producto"
    idProducto= Column(Integer, autoincrement=False, primary_key=True)
    nombre=Column(String,  autoincrement=False)
    componente=Column(String,  autoincrement=False)
    def __str__(self):
        return '{0}{1}{2}{3}'.format(self.idProducto,self.nombre,self.componente)

class DetalleProducto(Base2):
    __tablename__="detalleProducto"
    idDetalle= Column(Integer, autoincrement=False, primary_key=True)
    precio=Column(String,  autoincrement=False)
    fecha= Column(DateTime())
    farmacia=Column(String,  autoincrement=False)
    link=Column(String,  autoincrement=False)
    idProducto= Column(Integer, autoincrement=False, nullable=False)
    def __str__(self):
        return '{0}{1}{2}{3}'.format(self.idDetalle,self.precio,self.fecha, self.idProducto,self.farmacia,self.link)
  
meta_data.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

ContadorItems =0
sumID=0
sumIDP=0
for id in session.query(Productos.idProducto):
  sumID= id.idProducto
for id in session.query(DetalleProducto.idDetalle):
  sumIDP= id.idDetalle


contadorPagina=1
array = []
FarmaciaLocal="Farmacia Ahumada"
contadorWhile =0


IDProducto= list()
NombreP = list()
ComponenteP = list()
PrecioP = list()
IDProducto = list()
FarmaciaP = list()
LinkP = list()
FechaP = list()
IDProductoDB = list()
detalleProducto = list()
PrecioPActualizar = list()
FechaPActualizar = list()

def NuevoDatoID(ID):
  IDProducto.append(ID)
  return print(f'ID: {ID}')
def NuevoDatoNombre(Nombre):
  NombreP.append(Nombre)
  return print(f'Nombre: {Nombre}')
def NuevoDatoComponente(Componente):
  ComponenteP.append(Componente)
  return print(f'Componente: {Componente}')
def NuevoDatoPrecio(Precio):
  PrecioP.append(Precio)
  return print(f'Precio: {Precio}')
def NuevoDatoFarmacia(Farmacia):
  FarmaciaP.append(Farmacia)
  return print(f'Farmacia: {Farmacia}') 
def NuevoDatoLink(Link):
  LinkP.append(Link)
  return print(f'Link: {Link}') 
def NuevoDatoFecha(Fecha):
  FechaP.append(Fecha)
  return print(f'Fecha: {Fecha}',"\n-----------------------------------")  

def ProductoActualizado(ID):
  detalleProducto.append(ID)
  return print(f'ID Detalle: {ID}')
def IDProductoEncontrado(ID):
  IDProductoDB.append(ID)
  return print(f'ID Producto Encontrado: {ID}')
def ActualizarPrecio(Precio):
  PrecioPActualizar.append(Precio)
  return print(f'Precio Nuevo: {Precio}')
def ActualizarFecha(Fecha):
  FechaPActualizar.append(Fecha)
  return print(f'Fecha Nueva: {Fecha}',"\n-----------------------------------")


def NuevoProducto():
  df = pd.DataFrame({'idProducto': IDProducto, 'Nombre':NombreP, 'Componente': ComponenteP}, index=list(range(1,contadorWhile+1)))
  df.to_sql(con=engine, name=Productos.__tablename__, if_exists='append', index=False)
  df2 = pd.DataFrame({'idDetalle': detalleProducto, 'Precio': PrecioP, 'Fecha':FechaP, 'Farmacia': FarmaciaP, 'Link': LinkP, 'idProducto': IDProductoDB}, index=list(range(1,contadorWhile+1)))
  df2.to_sql(con=engine, name=DetalleProducto.__tablename__, if_exists='append', index=False)
def ActualizarProducto():
  df4 = pd.DataFrame({'idDetalle': detalleProducto, 'Precio': PrecioPActualizar, 'Fecha':FechaPActualizar, 'Farmacia': FarmaciaP, 'Link': LinkP, 'idProducto': IDProductoDB}, index=list(range(1,contadorWhile+1)))
  df4.to_sql(con=engine, name=DetalleProducto.__tablename__, if_exists='append', index=False)


ActualizarP=0
ProductoN=0
while ContadorItems <12:
    if(contadorPagina==2):
      break
    context = ssl._create_unverified_context()
    res = urlopen("https://www.farmaciasahumada.cl/medicamentos.html?p="+str(contadorPagina)+'', context=context)
    soup = BeautifulSoup(res, 'lxml')
    tabla = soup.findAll('a', {'class': 'product photo product-item-photo'})

    for linkst in tabla:
      ContadorItems+=1
      contadorWhile +=1
      sumID+=1
      sumIDP+=1
      if ContadorItems==12:
        ContadorItems=0
        contadorPagina+=1
      listado = linkst['href']
      
      #r = requests.get(listado)
      r= urlopen(listado, context=context)
      iteracion = BeautifulSoup(r, 'lxml')
      principio= ['Principio Activo']
      Nombre = iteracion.find('span', class_='base').text
      for resultadoNombre in session.query(Productos.nombre).filter_by(nombre=Nombre):
        nombreBD = resultadoNombre.nombre
      try:
        if(Nombre == nombreBD):
          ActualizarP += 1
          ProductoActualizado(sumIDP)
          for resultadoID in session.query(Productos.idProducto).filter_by(nombre=Nombre):
            idDB = resultadoID.idProducto
          IDProductoEncontrado(idDB)
          try:
            PrecioS = iteracion.find('span', class_='old-price').text.replace("Precio Internet","")
            Precio = PrecioS[4:]
            Precio = Precio.replace(".","")
            ActualizarPrecio(Precio.strip())
          except:
            PrecioS = iteracion.find('span', class_='price').text.replace("Precio Internet","")
            Precio = PrecioS[1:]
            Precio = Precio.replace(".","")
            ActualizarPrecio(Precio.strip())
          NuevoDatoFarmacia(FarmaciaLocal)
          NuevoDatoLink(listado)
          ActualizarFecha(fecha)
      except:
        ProductoN+=1
        NuevoDatoID(sumID)
        NuevoDatoNombre(Nombre)
        try:
          PrecioS = iteracion.find('span', class_='old-price').text.replace("Precio Internet","")
          Precio = PrecioS[4:]
          Precio = Precio.replace(".","")
          NuevoDatoPrecio(Precio.strip())
        except:
          PrecioS = iteracion.find('span', class_='price').text.replace("Precio Internet","")
          Precio = PrecioS[1:]
          Precio = Precio.replace(".","")
          NuevoDatoPrecio(Precio.strip())
        for td in iteracion.find_all("td"):
          if td.get('data-th') in principio:
            Componente = td
            NuevoDatoComponente(Componente.text)
        NuevoDatoFarmacia(FarmaciaLocal)
        NuevoDatoLink(listado)
        ProductoActualizado(sumIDP)
        IDProductoEncontrado(sumIDP)
        NuevoDatoFecha(fecha)
        
        

      
if(ProductoN >0):         
  NuevoProducto()    
if(ActualizarP >0):
  ActualizarProducto()
  


           

