'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 21/03/2022
 * Version: Python 3.7.0
 * Descripcion: programa que lee una imagen y realiza un binarizado de la misma aplicando un umbral determinado
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

#======================== Variable ====================================
ubicacion=""
img=np.zeros((512,512,1),np.uint8)
img_bin=np.zeros((512,512,1),np.uint8)

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
Funcion: obtener_binario
Descripcion: Permite realizar un binarizado de la imagen aplicando un umbral
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def obtener_binario():
    global img, barra, img_bin                              #Obtengo las variables globales
    img_bin=copy.deepcopy(img)                              #Copio imagen para no alterar la original
    for row in range (img_bin.shape[1]):                    #Recorro el ancho de la imagen
        for col in range (img_bin.shape[0]):                #Recorro el largo de la imagen
            if (img_bin[col][row]>barra.get()).all():       #Si el valor del pixel es mayor al de la barra
                img_bin[col][row]=255                       #Pongo el pixel en 255
            else:
                img_bin[col][row]=0                         #Sino pongo el pixel en 0
    cv2.namedWindow("Imagen binaria",cv2.WINDOW_NORMAL)     #Creo ventana para mostrar imagen procesada
    cv2.resizeWindow('Imagen binaria', 400, 300)            #Determino el tamaño de la ventana creada
    cv2.imshow('Imagen binaria',img_bin)                    #Imprimo la imagen en la ventana
    cambiar_texto_label2("Binario Listo", "green")          #Cambio texto y color del label2
    print("binario listo")                                  #Indico que termino el proceso por la consola


'''/*========================================================================
Funcion: Guardar_archivo
Descripcion: Permite guardar una imagen
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Guardar_archivo():
    global img_bin                                              #Obtengo las variables globales
    directorio=filedialog.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (('Archivo png', '.png'),('Archivo jpg', '.jpg'),("todos los archivos","*.*")),defaultextension='.png')  #Abro ventana para seleccionar ubicacion
    print("Ubicacion imagen binaria: ")             
    print(directorio)
    cv2.imwrite( directorio, img_bin)    #Guardo la imagen binaria o procesada
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

#bit = root.iconbitmap('icon.ico')
root.title('Practico2')
root.resizable(False, False)
root.geometry('300x230')
barra = DoubleVar()

#Describo boton abrir archivo
open_button = ttk.Button(
    root,
    text='Arbir archivo',
    command= Seleccionar_archivo
)

#Describo boton realizar binario
binario_button = ttk.Button(
    root,
    text='Realizar binario',
    command=lambda:[cambiar_texto_label2("Binarizando, por favor espere...", "red"), obtener_binario()]
    
)

#Describo boton Guardar archivo
guardar_button = ttk.Button(
    root,
    text='Guardar archivo',
    command=Guardar_archivo
)

#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
binario_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
guardar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
#genero un label y una barra de escala
label = Label(root,text="Umbral: ")
label.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
s2 = tk.Scale(root, variable = barra, from_=0, to=255, tickinterval=100, orient=tk.HORIZONTAL, length=300).pack()
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)



#Comienzo la aplicacion
root.mainloop()