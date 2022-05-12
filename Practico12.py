'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 06/05/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 *          Desarrollado en: Windows 10 x64
 * Descripcion: 
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk                            #Para ventana grafico
from tkinter import ttk                         #Para ventana grafico
from tkinter import *                           #Para ventana grafico
from tkinter import filedialog as filedialog
from turtle import distance    #Para abrir y guardar archivos
import numpy as np                              #Para tratar con numeros matematicos para opencv    
import cv2                                      #Librerira opencv
import copy                                     #Para poder copiar matrices

#======================== Variable ====================================
Nombre_app="Practico 12 - Burgos"
ubicacion=""

#======================== Implementaciones=============================

'''/*========================================================================
Funcion: Seleccionar_imagenes
Descripcion: Permite seleccionar 2 o mas fotos que se van a procesar
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Seleccionar_imagenes():
    global ubicacion                                            #Obtengo las variables globales
    ubicacion = filedialog.askopenfilename(title='Abrir archivos',initialdir='/', filetypes=(('Archivo png', '*.png*'),('Archivo jpg', '*.jpg')), multiple=True) #Obtengo la ruta seleccionada
    cambiar_texto_label2("Fotos seleccionadas", "green")       #Cambio texto y color del label2


'''/*========================================================================
Funcion: Alinear_imagenes
Descripcion: Alineacion de dos imagenes usando SIFT
Sin parametro de entrada
No retorna nada
========================================================================*/'''

def Alinear_imagenes():
    MIN_MATCH_COUNT = 10
    #img1 = cv2.imread(ubicacion[0] , 0)            #Leemos la imagen 1
    #img2 = cv2.imread(ubicacion[1] , 0)            #Leemos la imagen 2
    
    img1 = cv2.imread("C:/Users/fabia/OneDrive/Desktop/1.jpg" , 0)            #Leemos la imagen 1
    img2 = cv2.imread("C:/Users/fabia/OneDrive/Desktop/2.jpg" , 0)            #Leemos la imagen 2
    
    dscr = cv2.xfeatures2d.SIFT_create()           #Inicializamos el detector y el descriptor
    
    kp1 , des1 = dscr.detectAndCompute(img1, None) #Encontramos los puntos clave y los descriptores con SIFT en la imagen 1
    kp2 , des2 = dscr.detectAndCompute(img2, None) #Encontramos los puntos clave y los descriptores con SIFT en la imagen 2
    
    #Muestro los puntos claves encontrados
    img1 = cv2.drawKeypoints(img1, kp1, None)
    img2 = cv2.drawKeypoints(img2, kp2, None)

    #Para marcar puntos relacionados
    matchess =sorted(cv2.BFMatcher(cv2.NORM_L2).match(des1 , des2), key= lambda x:x.distance)
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matchess[:600], img2, flags=2)
    cv2.imshow('SIFT', img3)                         #Puntos relacionados

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    matches = matcher.knnMatch(des1 , des2 , k=2)
    #matches =sorted(cv2.BFMatcher(cv2.NORM_L2).match(des1 , des2), key= lambda x:x.distance)
    #cv2.imshow('Img1', img1)                         #Muestro el resultado
    #cv2.imshow('Img2', img2)                         #Muestro el resultado

    # Guardamos los buenos matches usando el test de razón de Lowe
    good = []
    
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    
    if(len(good) > MIN_MATCH_COUNT):
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1 , 1 , 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1 , 1 , 2)
        #print(dst_pts[1][0][0])
        #print(dst_pts)
        #for i in range(0, dst_pts.shape[0] - 1):
        #    dst_pts[i][0][0]=dst_pts[i][0][0]+200
        #print(dst_pts)
        #[[[386.4723   143.67966 ]],[[386.4723   143.67966 ]]]
        H, mask = cv2.findHomography( dst_pts , src_pts , cv2.RANSAC, 5.0) # Computamos la homografía con RANSAC
        
    rows2, cols2 = img2.shape[:2]
    
    wimg2 = cv2.warpPerspective(img2, H, (cols2,rows2)) #Aplico la transformación afín usando cv2.warpAffine()
    #rows2=rows2+300
   
    cv2.imshow('R3', wimg2)                             #Muestro el resultado
    # Mezclamos ambas imágenes
    alpha = 0.5
    blend = np.array(wimg2*alpha + img1*(1-alpha), dtype=np.uint8)
    cv2.imshow('Resultado', blend)                            #Muestro el resultado


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
root.title(Nombre_app)
root.resizable(False, False)
root.geometry('300x300')
id_generar = DoubleVar()

#Describo boton abrir archivo
open_button = ttk.Button(
    root,
    text='Seleccionar 2 imagenes',
    command= Seleccionar_imagenes
)


#Describo boton para visualizar video por realidad aumentada
Alinear= ttk.Button(
    root,
    text='Alinear imagenes',
    command=Alinear_imagenes
)



#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
Alinear.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

#Genero un label
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.mainloop()
