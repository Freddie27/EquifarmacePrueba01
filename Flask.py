from flask import Flask, render_template
from numpy.core.fromnumeric import prod
from numpy.lib.shape_base import row_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint
from datetime import datetime
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false, null
from sqlalchemy.orm import aliased
import pandas
from flask import request
from sqlalchemy.sql.schema import ForeignKeyConstraint
import csv
import pandas as pd
import numpy as np
from io import StringIO
from pandas import Timestamp
import datetime
from datetime import datetime
import re
import random
from datetime import date
from werkzeug.utils import redirect






# pyodbc stuff for MS SQL Server Express
driver='{ODBC Driver 17 for SQL Server}'
server='localhost\SQLEXPRESS'
#server='LAPTOP-PL59D9FT\SQLEXPRESS'
#server='DESKTOP-BBB8C6H\SQLEXPRESS'
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
#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(engine)
#file_name ='data/Salcobrand_WS_230.csv'
#df = pandas.read_csv(file_name)
#df.to_sql(con=engine, name=Productos.__tablename__, if_exists='append', index=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


app = Flask(__name__, static_url_path='/js')

@app.route("/", methods=['GET','POST'])
def principal():
    if request.method == 'GET':
        placeholder ="Nombre de medicamento..."
        return render_template("index2.html", placeholder=placeholder)
    elif request.method == 'POST':
        data = []
        NombreMed = request.form.get('NombreMed')
        nombreTabla = "Nombre"
        componenteTabla = "Componente"
        claseTabla="table data responsive table-light table-hover TablaResultado "
        q = session.query(Productos).filter(Productos.nombre.like('%'+NombreMed+'%'))
        for instance in q:
            NombrePorUsuario =instance.nombre
            for instances in session.query(Productos).order_by(Productos.idProducto).filter_by(nombre = NombrePorUsuario):
                data.append(instances)
        encontrado=False
        post = True
        if data:
            encontrado=True
        placeholder ="Nombre de medicamento..."
        return render_template("index2.html", data=data, post=post, encontrado=encontrado, placeholder=placeholder, NombreMed=NombreMed,  nombreTabla=nombreTabla, componenteTabla=componenteTabla, claseTabla=claseTabla)

headings= ("Nombre", "Componente", "Precio", "Farmacia")

@app.route("/productos",  methods=['GET','POST'])
def productos():
    if request.method =='GET':
        title = "Productos"
        data = []
        datainstance = []
        datainstance2 = []
        datainstance3 = []
        for instances in session.query(Productos).order_by(Productos.idProducto):
            datainstance.append(instances)
            datainstance3.append(instances.componente)
        datainstance3 = list(dict.fromkeys(datainstance3))
        for instances in session.query(DetalleProducto):
                datainstance2.append(instances.farmacia)
        datainstance2 = list(dict.fromkeys(datainstance2))
        return render_template('productos.html', title= title, headings= headings, data=data, datainstance=datainstance, datainstance2=datainstance2, datainstance3=datainstance3)
    elif request.method == 'POST':

        title = "Productos"
        data = []
        datainstance = []
        datainstance2 = []
        datainstance3 = []
        checkeds="checked"
        for instances in session.query(Productos).order_by(Productos.idProducto):
            datainstance3.append(instances.componente)
        datainstance3 = list(dict.fromkeys(datainstance3))
        for instances in session.query(DetalleProducto):
                datainstance2.append(instances.farmacia)
        datainstance2 = list(dict.fromkeys(datainstance2))
        try:
            ComponenteProducto = request.form['radioComponente']
            for instances in session.query(Productos).order_by(Productos.idProducto).filter_by(componente = ComponenteProducto):
                datainstance.append(instances)
            
            return render_template('productos.html', title= title, headings= headings, data=data, datainstance=datainstance, datainstance2=datainstance2, datainstance3=datainstance3, ComponenteProducto = ComponenteProducto, checkeds=checkeds)
        except:
            pass
        try:
            ComponenteFarmacia = request.form['radioFarmacia']
            idds=list()
            for instances in session.query(DetalleProducto.idProducto).order_by(DetalleProducto.idProducto).filter_by(farmacia = ComponenteFarmacia):
                idds= (instances.idProducto)
                for instances in session.query(Productos).filter_by(idProducto=idds):
                    datainstance.append(instances)
            return render_template('productos.html', title= title, headings= headings, data=data, datainstance=datainstance, datainstance2=datainstance2, datainstance3=datainstance3,ComponenteFarmacia = ComponenteFarmacia)
        except:
            pass
        NombreProducto = request.form.get('NombreProducto')
        precioP = list()
        for data in session.query(Productos).filter_by(nombre=NombreProducto):
            IDProducto = data.idProducto
            ComponenteProducto = data.componente
            FarmaciaProducto = data.farmacia
            for data2 in session.query(DetalleProducto).order_by(DetalleProducto.precio).filter_by(idProducto = IDProducto):
                 precioP.append(data2.precio)
            return render_template('producto_clicked.html', IDProducto = IDProducto, NombreProducto = NombreProducto, ComponenteProducto = ComponenteProducto, FarmaciaProducto = FarmaciaProducto, precioP = precioP)




@app.route("/producto_clicked",  methods=['GET', 'POST'])
def producto_clicked():
    if request.method == 'GET':
        NombreProducto = request.args.get('botonCarrusel')
        farmaciaP =list()
        labels=list()
        PrecioP=list()
        Precio1P=list()
        Precio2P=list()
        Similares=list()
        claseTabla="table table-hover table-light tablaSB"
        for data in session.query(Productos).filter_by(nombre=NombreProducto):
            IDProducto = data.idProducto
            ComponenteProducto = data.componente
        for data2 in session.query(DetalleProducto).order_by(DetalleProducto.precio).filter_by(idProducto = IDProducto):
            PrecioP.append(data2.precio)
            farmaciaP.append(data2.farmacia)
            precioP = PrecioP[0]
        sql_query = pd.read_sql_query ('''SELECT * FROM detalleProducto where idProducto='''+str(IDProducto)+'''''', engine)
        df = pd.DataFrame(sql_query, columns = ['precio', 'fecha', 'farmacia', 'idProducto'])
        fecha = df['fecha'].values.tolist()
        for f in fecha:
            labels.append(str(f))
            labels = list(dict.fromkeys(labels))
        FRed = False
        FAhu = False
        FRaa = False
        titulo1=""
        titulo2=""
        try:
            for data in session.query(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia="Farmacia Ahumada"):
                Precio1P.append(data.precio)
                FAhu=True
                titulo1 ="Farmacia Ahumada"
        except:
            pass
        try:
            for data2 in session.query(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia="Farmacia RedFarma"):
                Precio2P.append(data2.precio)
                FRed=True
                titulo2 ="Farmacia RedFarma"
        except:
            pass
        f1="Precio"
        formato=""
        nombre=""
        com=""
        grss=""
        num=""
        aux = False
        aux2=False
        contt=0
        try:
            if aux==False:
                #tipo1
                a =(re.findall('^[\w]+ x',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        
        try:
            if aux==False:
                #tipo2
                a =(re.findall('^[\w]+ \D+',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        try:
            if aux==False:
                #tipo3
                a =(re.findall('^[\w]+ ',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        try:
            if aux==False:
                #tipo4
                a =(re.findall('^[\w]+-[\w]+',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        if contt ==1:
            #excepcion1
            a =(re.findall('^[\w]+ ',NombreProducto))
            for b in a:
                nombre = b
        else:
            for b in a:
                nombre = b

        #Regex para separar formato
        try:
            if aux2==False:
                #tipo1
                a =(re.findall('[\ ]+x[\d]+\D+[\d]+ \w+',NombreProducto))
                if a:
                    aux2 = True
                else:
                    aux2=False
        except:
            pass
        
        try:
            if aux2==False:
                #tipo2
                a =(re.findall('[\ ]+\d[ +.%/\w,-]+',NombreProducto))
                if a:
                    aux2 = True
                else:
                    aux2=False
        except:
            pass
        for b in a:
            formato = b.strip()
        try:

            comp =(re.findall('[comp]+',NombreProducto))
            for comps in comp:
                com = comps
                break
        except:
            pass
        try:

            gr =(re.findall('[gr]+',NombreProducto))
            for grs in gr:
                grss = grs
                break
        except:
            pass
        try:
            numero =(re.findall('[\d]+',NombreProducto))
            for nums in numero:
                num = nums
                break
        except:
            pass
        data=[]
        data2=[]
        adalias2 = aliased(DetalleProducto)
        q = session.query(Productos).filter(Productos.componente.like('%'+ComponenteProducto+'%'))
        
        nombrelist =list()
        cont=0
        for instances in session.query(DetalleProducto).order_by(DetalleProducto.fecha.desc()).filter_by(idProducto = IDProducto):
            fechaBD = instances.fecha
        for instance in q:
            nombrelist.append(instance)
        for nomli in nombrelist:
            q1 = session.query(Productos.nombre, adalias2.precio).filter(adalias2.idProducto==nomli.idProducto).filter(adalias2.fecha==fechaBD).filter(Productos.nombre == nomli.nombre).filter(Productos.nombre != NombreProducto).order_by(adalias2.precio)
            for qq in q1:
                cont += 1
                data.append(qq)
                break
        print(cont)
        width = 200 * cont
        height="220px"
        if width > 1000:
            width = "1000px"
            height="203px"
        Similares = list(dict.fromkeys(data))
        precioAhumada = False
        precioRedFarma = False
        data3=""
        data4=""
        data5=""
        data6=""
        link=""
        link2=""
        try:
            for instances in session.query(DetalleProducto).order_by(DetalleProducto.fecha).order_by(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia = "Farmacia Ahumada"):
                    data3 = instances.farmacia
                    data4 = instances.precio
                    link = instances.link
                    precioAhumada = True
        except:
            pass
        try:
            for instances in session.query(DetalleProducto).order_by(DetalleProducto.fecha).order_by(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia = "Farmacia RedFarma"):
                    data5 = instances.farmacia
                    data6 = instances.precio
                    link2 = instances.link
                    precioRedFarma = True
        except:
            pass
        return render_template('producto_clicked.html',height=height,width=width,claseTabla=claseTabla, data2=data2,precioAhumada=precioAhumada, precioRedFarma=precioRedFarma,data3=data3, data4=data4, data5=data5, data6=data6, link=link, link2 = link2,labels=labels, titulo1=titulo1, titulo2=titulo2, Precio1P=Precio1P, Precio2P=Precio2P, FRed=FRed, FAhu=FAhu, FRaa=FRaa,  NombreProducto = nombre, FormatoProducto=formato, ComponenteProducto = ComponenteProducto, farmaciaP = farmaciaP, precioP = precioP, Similares=Similares)
    elif request.method == 'POST':
        NombreProducto = request.form.get('NombreProducto')
        
        farmaciaP =list()
        labels=list()
        PrecioP=list()
        Precio1P=list()
        Precio2P=list()
        Similares=list()
        claseTabla="table table-hover table-light"
        for data in session.query(Productos).filter_by(nombre=NombreProducto):
            IDProducto = data.idProducto
            ComponenteProducto = data.componente
        for data2 in session.query(DetalleProducto).order_by(DetalleProducto.precio).filter_by(idProducto = IDProducto):
            PrecioP.append(data2.precio)
            farmaciaP.append(data2.farmacia)
            precioP = PrecioP[0]
        sql_query = pd.read_sql_query ('''SELECT * FROM detalleProducto where idProducto='''+str(IDProducto)+'''''', engine)
        df = pd.DataFrame(sql_query, columns = ['precio', 'fecha', 'farmacia', 'idProducto'])
        fecha = df['fecha'].values.tolist()
        for f in fecha:
            labels.append(str(f))
            labels = list(dict.fromkeys(labels))
        FRed = False
        FAhu = False
        FRaa = False
        titulo1=""
        titulo2=""
        try:
            for data in session.query(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia="Farmacia Ahumada"):
                Precio1P.append(data.precio)
                FAhu=True
                titulo1 ="Farmacia Ahumada"
        except:
            pass
        try:
            for data2 in session.query(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia="Farmacia RedFarma"):
                Precio2P.append(data2.precio)
                FRed=True
                titulo2 ="Farmacia RedFarma"
        except:
            pass
        f1="Precio"
        formato=""
        nombre=""
        com=""
        grss=""
        num=""
        aux = False
        aux2=False
        contt=0
        #Regex para separar nombre
        try:
            if aux==False:
                #tipo1
                a =(re.findall('^[\w]+ x',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        
        try:
            if aux==False:
                #tipo2
                a =(re.findall('^[\w]+ \D+',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        try:
            if aux==False:
                a =(re.findall('^[\w]+ ',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        try:
            if aux==False:
                a =(re.findall('^[\w]+-[\w]+',NombreProducto))
                contt+=1
                if a:
                    aux = True
                else:
                    aux=False
        except:
            pass
        if contt ==1:
            a =(re.findall('^[\w]+ ',NombreProducto))
            for b in a:
                nombre = b
        else:
            for b in a:
                nombre = b

        try:
            if aux2==False:
                #tipo1
                a =(re.findall('[\ ]+x[\d]+\D+[\d]+ \w+',NombreProducto))
                if a:
                    aux2 = True
                else:
                    aux2=False
        except:
            pass
        
        try:
            if aux2==False:
                #tipo2
                a =(re.findall('[\ ]+\d[ +.%/\w,-]+',NombreProducto))
                if a:
                    aux2 = True
                else:
                    aux2=False
        except:
            pass
        for b in a:
            formato = b.strip()
        try:

            comp =(re.findall('[comp]+',NombreProducto))
            for comps in comp:
                com = comps
                break
        except:
            pass
        try:

            gr =(re.findall('[gr]+',NombreProducto))
            for grs in gr:
                grss = grs
                break
        except:
            pass
        try:
            numero =(re.findall('[\d]+',NombreProducto))
            for nums in numero:
                num = nums
                break
        except:
            pass
        data=[]
        data2=[]
        adalias2 = aliased(DetalleProducto)
        q = session.query(Productos).filter(Productos.componente.like('%'+ComponenteProducto+'%'))
        nombrelist =list()
        cont=0
        for instances in session.query(DetalleProducto).order_by(DetalleProducto.fecha.desc()).filter_by(idProducto = IDProducto):
            fechaBD = instances.fecha
        for instance in q:
            nombrelist.append(instance)
            
        for nomli in nombrelist:
            q1 = session.query(Productos.nombre, adalias2.precio).filter(adalias2.idProducto==nomli.idProducto).filter(adalias2.fecha==fechaBD).filter(Productos.nombre == nomli.nombre).filter(Productos.nombre != NombreProducto).order_by(adalias2.precio)
            for qq in q1:
                cont += 1
                data.append(qq)
                break
        print(cont)
        width = 200 * cont
        height="220px"
        if width > 1000:
            width = "1000px"
            height="203px"
        Similares = list(dict.fromkeys(data))
        precioAhumada = False
        precioRedFarma = False
        data3=""
        data4=""
        data5=""
        data6=""
        link=""
        link2=""
        try:
            for instances in session.query(DetalleProducto).order_by(DetalleProducto.fecha).order_by(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia = "Farmacia Ahumada"):
                    data3 = instances.farmacia
                    data4 = instances.precio
                    link = instances.link
                    precioAhumada = True
        except:
            pass
        try:
            for instances in session.query(DetalleProducto).order_by(DetalleProducto.fecha).order_by(DetalleProducto.precio).filter_by(idProducto = IDProducto).filter_by(farmacia = "Farmacia RedFarma"):
                    data5 = instances.farmacia
                    data6 = instances.precio
                    link2 = instances.link
                    precioRedFarma = True
        except:
            pass
        return render_template('producto_clicked.html',width=width,height=height, cont=cont,claseTabla=claseTabla, data2=data2,precioAhumada=precioAhumada, precioRedFarma=precioRedFarma,data3=data3, data4=data4, data5=data5, data6=data6, link=link, link2 = link2, labels=labels, titulo1=titulo1, titulo2=titulo2, Precio1P=Precio1P, Precio2P=Precio2P, FRed=FRed, FAhu=FAhu, FRaa=FRaa,  NombreProducto = nombre, FormatoProducto=formato, ComponenteProducto = ComponenteProducto, farmaciaP = farmaciaP, precioP = precioP, Similares=Similares)


@app.route('/url_producto',  methods=['GET', 'POST'])
def url_producto():
     if request.method == 'POST':
        Link = request.form.get('botonLink')
        Link= "https://"+Link
        return redirect(Link)


if __name__ == "__main__":
    app.run()
#"""
