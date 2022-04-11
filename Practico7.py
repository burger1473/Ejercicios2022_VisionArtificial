'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 11/04/2022
 * Version: Python 3.7.0
 * Descripcion: programa que realiza la transformacion similaridad a una imagen
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk                            #Para ventana grafico
from tkinter import ttk                         #Para ventana grafico
from tkinter import *                           #Para ventana grafico
from tkinter import filedialog as filedialog    #Para abrir y guardar archivos
from tkinter.messagebox import showinfo         #Para menasajes popout
import os                                       #Para operaciones del sistema    
import cv2                                      #Librerira opencv
import numpy as np                              #Para tratar con numeros matematicos para opencv
import copy                                     #Para poder copiar matrices
import math                                     #Para usar coseno  seno

#======================== Variable ====================================
ubicacion=""
img=np.zeros((512,512,1),np.uint8)
img_modif=np.zeros((512,512,1),np.uint8)

#======================== Implementaciones=============================

'''/*========================================================================
Funcion: Seleccionar_archivo
Descripcion: Permite seleccionar una imagen y la muestra
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def  Seleccionar_archivo():
    global img                                             #Obtengo las variables globales
    filename = filedialog.askopenfilename(title='Abrir archivo',initialdir='/', filetypes=(('Archivo png', '*.png*'),('Archivo jpg', '*.jpg'))) #Obtengo la ruta seleccionada
    ubicacion=filename
    print("Ubicacion imagen orginal: ")
    print(ubicacion)
    img = cv2.imread( ubicacion , 1)                        #Obtengo la imagen de la ubicacion seleccionada
    cv2.namedWindow("Imagen original",cv2.WINDOW_NORMAL)    #Creo ventana para mostrar imagen procesada
    cv2.resizeWindow('Imagen original', 400, 300)           #Determino el tamaño de la ventana creada
    cv2.imshow('Imagen original',img)                       #Imprimo la imagen en la ventana
    

'''/*========================================================================
Funcion: transformar
Descripcion: Permite realizar una transformacion Euclidiana
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def transformar():
    global img, img_modif, angulo, traslacion_x, traslacion_y #Obtengo las variables globales
    global escala                                             #Obtengo las variables globales
    img_modif=copy.deepcopy(img)                              #Copio imagen para no alterar la original
    (h, w) = (img_modif.shape[0], img_modif.shape[1])         #Obtengo tamaño imagen
    centro= (w/2, h/2)                                        #Obtengo centro imagen
   
    metodo= 1                                                 #Indico metodo a utilizar

    #METODO1
    if metodo==1:
        M= cv2.getRotationMatrix2D(centro, angulo.get(), escala.get())   #Obtengo una matriz 2x3 de rotacion
        M[0][2]=M[0][2]+traslacion_x.get()                         #Le sumo la traslacion en x
        M[1][2]=M[1][2]+traslacion_y.get()                         #Le sumo la traslacion en y
    
    #METODO2
    if metodo==2:
        #Genero manualmente la matriz de transformación 
        M=np.float32([[escala.get()*math.cos(math.radians (angulo.get())), escala.get()*math.sin(math.radians (angulo.get())), traslacion_x.get()],
                 [-escala.get()*math.sin(math.radians (angulo.get())), escala.get()*math.cos(math.radians (angulo.get())), traslacion_y.get()]])
    

    shifted =cv2.warpAffine(img_modif, M, (w, h))
    #print(M)                  
    cv2.namedWindow("Imagen transformada",cv2.WINDOW_NORMAL)       #Creo ventana para mostrar imagen procesada
    cv2.resizeWindow('Imagen transformada', 400, 300)              #Determino el tamaño de la ventana creada
    cv2.imshow('Imagen transformada',shifted)                    #Imprimo la imagen en la ventana
    cambiar_texto_label2("Transformacion lista", "green")            #Cambio texto y color del label2
    print("Transformacion lista")                                    #Indico que termino el proceso por la consola


'''/*========================================================================
Funcion: Guardar_archivo
Descripcion: Permite guardar una imagen
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Guardar_archivo():
    global img_modif                                              #Obtengo las variables globales
    directorio=filedialog.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (('Archivo png', '.png'),('Archivo jpg', '.jpg'),("todos los archivos","*.*")),defaultextension='.png')  #Abro ventana para seleccionar ubicacion
    print("Ubicacion imagen binaria: ")             
    print(directorio)
    cv2.imwrite( directorio, img_modif)    #Guardo la imagen binaria o procesada
    #showinfo.showinfo("Practico2", "Guardado con exito") # título, mensaje
    cambiar_texto_label2("Guardado con exito", "black")         #Cambio texto y color de label2


'''/*========================================================================
Funcion: cambiar_texto_label2
Descripcion: Permite cambiar texto y color del label2
Parametro de entrada:
                     texto: string de texto que se desea escribir
                     color: color primario que se desea colocar al texto
No retorna nada
========================================================================*/'''
def cambiar_texto_label2(texto, color):
    label2.config(text = texto, fg=color)   #Cambia texto y color al label2
    root.update()                           #Actualiza los cambios instantaneamente

#======================== Configuracion grafica =============================

# Creo el root de windows
root = tk.Tk()
angulo = DoubleVar()
traslacion_x = DoubleVar()
traslacion_y = DoubleVar()
escala = DoubleVar()
bit = root.iconbitmap('icon.ico')
root.title('Practico6')
root.resizable(False, False)
root.geometry('300x500')


#Describo boton abrir archivo
open_button = ttk.Button(
    root,
    text='Arbir archivo',
    command= Seleccionar_archivo
)

#Describo boton realizar binario
accion_button = ttk.Button(
    root,
    text='Realizar Euclidiana',
    command=lambda:[cambiar_texto_label2("Realizando transformacion...", "red"), transformar()]
    
)

#Describo boton Guardar archivo
guardar_button = ttk.Button(
    root,
    text='Guardar archivo',
    command=Guardar_archivo
)

#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
accion_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
guardar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
#genero un label y una barra de escala
label = Label(root,text="Angulo: ")
label.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
s2 = tk.Scale(root, variable = angulo, from_=0, to=90, tickinterval=20, orient=tk.HORIZONTAL, length=300).pack()
label3 = Label(root,text="Traslacion x: ")
label3.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
s3 = tk.Scale(root, variable = traslacion_x, from_=0, to=255, tickinterval=100, orient=tk.HORIZONTAL, length=300).pack()
label4 = Label(root,text="Traslacion y: ")
label4.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
s4 = tk.Scale(root, variable = traslacion_y, from_=0, to=255, tickinterval=100, orient=tk.HORIZONTAL, length=300).pack()
label5 = Label(root,text="Escala imagen: ")
label5.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
s5 = tk.Scale(root, variable = escala, from_=0, to=3, tickinterval=0.5, resolution =   0.1, orient=tk.HORIZONTAL, length=300).pack()


label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)



#Comienzo la aplicacion
root.mainloop()