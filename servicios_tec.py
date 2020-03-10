## Se requiere importar para conectarse a MySQL
import mysql.connector as mysql
#Libreria para llamar al sistema operativo
import os
#Libreria y utilidades para la interfaz gráfica
import tkinter as tk 
from tkinter import ttk
from tkinter import scrolledtext

conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='puertos' )
operacion = conexion.cursor(buffered=True)

def getn():
    f = open("archivo.txt", "r")
    b = open("things.txt", "w")
    while(True):
        linea = f.readline()
        if not linea.find('PORT     STATE SERVICE'):
            linea = f.readline()
            while(linea.find('\n')):
                b.write(linea)
                linea = f.readline()
                if not linea:
                    break
        if not linea:
            break
    f.close()
    b.close()

def insertar():
    f = open ("things.txt","r")
    while(True):
        c=0
        c1=1
        port=""
        state=""
        service=""
        linea = f.readline()
        if(len(linea)==0):
            linea = f.readline()
        else:
            while (c1==1 and linea[c]!=' '):
                port+=linea[c]
                c+=1
            print(port)
            c1+=1
            while (linea[c]==' '):
                c+=1
            while (c1==2 and linea[c]!=' '):
                state+=linea[c]
                c+=1
            print(state)
            c1+=1
            while (linea[c]==' '):
                c+=1
            while (c1==3 and c<len(linea)):
                service+=linea[c]
                c+=1
            print(service)
            c1+=1
        #conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='puertos' )
        #operacion = conexion.cursor()
        operacion.execute( "INSERT INTO dato (puerto, estado, servicio) VALUES (\""+port+"\",\""+state+"\",\""+service+"\")" )
        conexion.commit()
        
        if not linea:
            break
        


computadora="192.168.1.6"
arch="archivo.txt"
os.system("nmap -oN "+arch+' '+computadora)
getn()
insertar()
# hacer la interfaz gráfica
#Ventana
ventana = tk.Tk()
ventana.title("PUERTOS RECONOCIDOS") 
#Controlar tamaño ventana
ventana.resizable(0,0)
#Poner un anuncio
ttk.Label(ventana, text="Solamente se muestra la información obtenida de un equipo").grid(column=0,row=0)
ttk.Label(ventana, text="Equipo analizado: "+computadora).grid(column=0,row=1)

#Configurar caja de texto
scrol_ancho= 60
scrol_alto= 50
#Ahora metemos la caja
caja = scrolledtext.ScrolledText(ventana, width= scrol_ancho, height=scrol_alto,wrap=tk.WORD)
caja.grid(column=0,columnspan=3)
operacion.execute( "SELECT * FROM dato")
conexion.commit()
for puerto, estado, servicio in operacion.fetchall() :
    caja.insert(tk.INSERT,(puerto, estado, servicio))
conexion.close()
#Activar ventana
ventana.mainloop()