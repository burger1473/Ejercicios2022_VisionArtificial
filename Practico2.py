'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 21/03/2022
 * Version: Python 3.7.0
 * Descripcion: programa que lee una imagen y realiza un binarizado de la misma aplicando un umbral determinado
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as filedialog
from tkinter.messagebox import showinfo
import os
import cv2
import numpy as np

#======================== Variable ====================================
ubicacion=""
img=np.zeros((512,512,1),np.uint8)


#======================== Implementaciones=============================

'''/*========================================================================
Funcion: Seleccionar_archivo
Descripcion: Permite seleccionar una imagen y la muestra
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def  Seleccionar_archivo():
    global img
    filename = filedialog.askopenfilename(title='Abrir archivo',initialdir='/', filetypes=(('Archivo jpg', '*.jpg'),('Archivo png', '*.png*')))
    ubicacion=filename
    print("Ubicacion imagen orginal: ")
    print(ubicacion)
    img = cv2.imread( ubicacion , 0)
    cv2.namedWindow("Imagen original",cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagen original', 400, 300)
    cv2.imshow('Imagen original',img)

'''/*========================================================================
Funcion: obtener_binario
Descripcion: Permite realizar un binarizado de la imagen aplicando un umbral
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def obtener_binario():
    global img, barra
    for row in img:
        for col in img:
            if (img[col][row]>barra.get()).all():
                img[col][row]=255
            else:
                img[col][row]=0
    cv2.namedWindow("Imagen binaria",cv2.WINDOW_NORMAL) 
    cv2.resizeWindow('Imagen binaria', 400, 300)          
    cv2.imshow('Imagen binaria',img)
    print("binario listo")


'''/*========================================================================
Funcion: Guardar_archivo
Descripcion: Permite guardar una imagen
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Guardar_archivo():
    global img
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)
    print("Ubicacion imagen binaria: ")
    print(directorio)
    cv2.imwrite( directorio +'/resultado_bin.png' , img)
    showinfo.showinfo("Practico2", "Guardado con exito") # título, mensaje



#======================== Configuracion grafica =============================

# Creo el root de windows
root = tk.Tk()
root.title('Practico2')
root.resizable(False, False)
root.geometry('300x180')
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
    command=obtener_binario
)

#Describo boton Guardar archivo
guardar_button = ttk.Button(
    root,
    text='Guardar archivo',
    command=Guardar_archivo
)

#Implemento los botones en el root
open_button.pack(expand=True)
binario_button.pack(expand=True)
guardar_button.pack(expand=True)
#genero un label y una barra de escala
label = Label(root,text="Umbral: ")
label.pack()
s2 = tk.Scale(root, variable = barra, from_=0, to=255, tickinterval=100, orient=tk.HORIZONTAL, length=300).pack()


#Comienzo la aplicacion
root.mainloop()