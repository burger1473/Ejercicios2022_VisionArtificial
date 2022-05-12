'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 06/05/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 *          Desarrollado en: Windows 10 x64
 * Descripcion: Este software permite abrir dos imagenes y unirlas generando una
 *              vista panoramica. Las imagenes tienen que ser especificas para unir.
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
MIN_MATCH_COUNT = 10
panoramica = np.zeros((512, 512, 3),np.uint8)

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
Funcion: hconcat_resize_min
Descripcion: Sirve para unir dos imagenes de diferente tamaño una al lado de la otra
Parametro de entrada: im_list: Lista con la ubicacion de las imagenes
Retorna: La imagen unida
========================================================================*/'''
def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)


'''/*========================================================================
Funcion: Alinear_imagenes
Descripcion: Alineacion de dos imagenes usando SIFT
Sin parametro de entrada
No retorna nada
========================================================================*/'''

def Alinear_imagenes():
    global MIN_MATCH_COUNT, alpha, panoramica                  #Variables globales
    
    if len(ubicacion)!=2:                                             #Si se selecciono mas de 2 imagenes o menos de 2 imagenes
        cambiar_texto_label2("Cantidad de imagenes erronea", "red")   #Escribo en label2
        return                                                        #Regreso y salgo de la funcion

    img1 = cv2.imread(ubicacion[0] , 1)                         #Leemos la imagen 1
    img2 = cv2.imread(ubicacion[1] , 1)                         #Leemos la imagen 2

    imganes_juntas = hconcat_resize_min([img1, img2])           #Uno las dos imagenes una al lado de la otra
    cv2.imshow('Imagenes originales', imganes_juntas)           #Muestro el resultado
    dscr = cv2.xfeatures2d.SIFT_create()                        #Inicializamos el detector y el descriptor
    
    kp1 , des1 = dscr.detectAndCompute(img1, None)              #Encontramos los puntos clave y los descriptores con SIFT en la imagen 1
    kp2 , des2 = dscr.detectAndCompute(img2, None)              #Encontramos los puntos clave y los descriptores con SIFT en la imagen 2
    
    #Muestro los puntos claves encontrados
    img1_keypoints = cv2.drawKeypoints(img1, kp1, None)         #Dibujo los puntos encontrados en imagen 1
    img2_keypoints = cv2.drawKeypoints(img2, kp2, None)         #Dibujo los puntos encontrados en imagen 2
    #cv2.imshow('Img1', img1_keypoints)                         #Muestro el resultado
    #cv2.imshow('Img2', img2_keypoints)                         #Muestro el resultado

    #Relaciono los puntos encontrados con emparejador o igualador (match)
    matcher = cv2.BFMatcher(cv2.NORM_L2)                        #Creo match
    matches = matcher.knnMatch(des1 , des2 , k=2)               #Obtengo puntos relacionados
    
    #Guardamos los buenos matches usando el test de razón de Lowe en la variable good
    good = []

    for m, n in matches:                                        #Recorro matches y obtengo m y n
        if m.distance < 0.7*n.distance:                         #Filtro por las distancia de los puntos
            good.append(m)                                      #Guardo el valor del punto en el arreglo good
    
    if(len(good) > MIN_MATCH_COUNT):                                                                 #Si existen suficientes puntos luego del filtrado
        img3 = cv2.drawMatches(img1_keypoints, kp1, img2_keypoints, kp2, good[:600], img2, flags=2)  #Para marcar puntos relacionados
        cv2.imshow('Puntos iguales filtrados', img3)                                                 #Para mostrar puntos relacionados
        
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1 , 1 , 2)                 #Obtengo los puntos para la homografia
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1 , 1 , 2)                 #Obtengo los puntos para la homografia
       
        H, mask = cv2.findHomography( dst_pts , src_pts , cv2.RANSAC, 5.0)  #Computamos la homografía para obtener la matriz de transformacion con RANSAC
        
        rows = img2.shape[0] + img1.shape[0]                                #El tamaño de salida es el conjunto de las dos imagenes
        cols = img2.shape[1] + img1.shape[1]                                #El tamaño de salida es el conjunto de las dos imagenes
        Perspectiva = cv2.warpPerspective(img2, H, (cols,rows))             #Aplico la transformación afín usando cv2.warpAffine()
        
        # Mezclamos ambas imágenes
        alpha2=alpha.get()/100                                              #Paso variable de porcentaje a valor
        copia = Perspectiva.copy()*alpha2                                   #Copia para no alterar imagen original
        copia[:img1.shape[0],:img1.shape[1]] +=  img1*(1-alpha2)            #Inserto valores de la imagen1 en la imagen con la perspectiva modificada tamaño perspectiva>img1  (750,1000,3)>(375,500,3)
        copia=np.array(copia,dtype=np.uint8)                                #Convierto los datos a tipo entero sin signo de 8 bit
        #blend = np.array(wimg2*alpha + img1*(1-alpha), dtype=np.uint8)     #Esta no sirve ya que las dos matrices son de diferente tamaño
        #cv2.imshow('Resultado', d)                                         #Muestro el resultado sin recortar con bordes negros
        recorte = copia[0:int(rows/2), 0:cols]                              #Recorto el resultado solo en eje y
        cv2.imshow("Resultado recortado", recorte)                          #Muestro el resultado recortado
        cambiar_texto_label2("Proceso terminado", "green")                  #Escribo en label2
        panoramica = recorte                                                #Paso imagen local a global para poder guardarla


'''/*========================================================================
Funcion: Guardar_imagen
Descripcion: Permite guardar una imagen
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Guardar_imagen():
    global panoramica                                                     #Obtengo las variables globales
    directorio=filedialog.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (('Archivo png', '.png'),('Archivo jpg', '.jpg'),("todos los archivos","*.*")),defaultextension='.png')  #Abro ventana para seleccionar ubicacion
    cv2.imwrite( directorio, panoramica)                                  #Guardo la imagen binaria o procesada
    #showinfo.showinfo("Practico2", "Guardado con exito")                 #Título, mensaje
    cambiar_texto_label2("Guardado con exito", "black")                   #Cambio texto y color de label2


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
alpha =DoubleVar()
alpha.set(50)
#bit = root.iconbitmap('icon.ico')
root.title(Nombre_app)
root.resizable(False, False)
root.geometry('300x230')
id_generar = DoubleVar()

#Describo boton abrir archivo
open_button = ttk.Button(root, text='Seleccionar 2 imagenes', command= Seleccionar_imagenes)

#Describo boton para visualizar video por realidad aumentada
Alinear= ttk.Button(root, text='Alinear imagenes', command=Alinear_imagenes)

#Describo boton para guardar recorte
guardar_button = ttk.Button(root, text='Guardar imagen alineada', command=Guardar_imagen)

#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
Alinear.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
guardar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

s1 = tk.Scale(root, variable = alpha, from_=0, to=100, tickinterval=20, resolution =   1, orient=tk.HORIZONTAL, length=300, label = "Mezclar con un alpha de: (%)").pack()

#Genero un label
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.mainloop()