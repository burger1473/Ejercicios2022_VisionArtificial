'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 18/04/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 * Descripcion: Medición de objetos
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk                            #Para ventana grafico
from tkinter import ttk                         #Para ventana grafico
from tkinter import *                           #Para ventana grafico
from tkinter import filedialog as filedialog    #Para abrir y guardar archivos
import numpy as np                              #Para tratar con numeros matematicos para opencv    
import cv2                                      #Librerira opencv
import copy                                     #Para poder copiar matrices
import os                                       #Para operaciones del sistema  
import math                                     #Para calculos matematicos

#======================== Variable ====================================
Nombre_app="Practico 10 - Burgos"
ubicacion=""
img = np.zeros((512, 512, 3),np.uint8)
img_mod = np.zeros((512, 512, 3),np.uint8)
img_dos = np.zeros((512, 512, 3),np.uint8)
img_transformada = np.zeros((512, 512, 3),np.uint8)
img_transformada_mod = np.zeros((512, 512, 3),np.uint8)
cant_puntos = 0
puntos = [[0,0],[0,0],[0,0],[0,0]]
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press ’m’ to toggle to curve
ix= -1
iy= -1
fx= -1
fy= -1
#======================== Implementaciones=============================

'''/*========================================================================
Funcion: Keyboardpress 
Descripcion: Funcion a la cual se llama por algun evento producido por el teclado
Parameto de entrada: key: tecla presionada
No retorna nada
========================================================================*/'''
def Keyboardpress( key):
    key_char = key.char 
    print(key_char,"fue presionado")
    #Series de if para cada letra que deseamos accionar
    if key_char == 'g':
        Guardar_imagen()
    if key_char == 'q':
        cv2.destroyAllWindows()     #Cierro las ventans de opencv
        root.destroy()              #Destruyo la aplicacion 


'''/*========================================================================
Funcion: transformación
Descripcion: Realiza el rectificado de una imagen y la incrusta en otra
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def transformacion():
    global img, puerta_ancho, puerta_alto, mts_to_pixel, img_transformada
    rows2, cols2 = img.shape[:2]    #Tamaño de la imagen original

    #Defino los 4 pares de puntos correspondientes
    input_pts = np.float32([[puntos[0][0],puntos[0][1]], [puntos[1][0],puntos[1][1]], [puntos[2][0],puntos[2][1]], [puntos[3][0],puntos[3][1]]])
    output_pts = np.float32([[0,0], [puerta_ancho.get()*mts_to_pixel.get(),0], [puerta_ancho.get()*mts_to_pixel.get(),puerta_alto.get()*mts_to_pixel.get()], [0,puerta_alto.get()*mts_to_pixel.get()]])

    #Calcule la matriz de transformación usando cv2.getPerspectiveTransfor()
    M= cv2.getPerspectiveTransform(input_pts , output_pts)
    #M[0][2]=M[0][2]+puntos[0][0]                       #Le sumo la traslacion en x
    #M[1][2]=M[1][2]+puntos[0][1]                       #Le sumo la traslacion en x

    #Aplico la transformación afín usando cv2.warpAffine()
    img_transformada = cv2.warpPerspective(img, M, (cols2,rows2),flags=cv2.INTER_LINEAR)

    
    
    cv2.namedWindow('Resultado')                                  #Indico nombre de la ventana
    cv2.setMouseCallback ('Resultado',callback2)                  #Establesco evento de mause sobre la ventana
    cv2.imshow('Resultado', img_transformada)                     #Muestro el resultado
    cambiar_texto_label2("Proceso finalizado", "green")           #Cambio texto y color de label2


'''/*========================================================================
Funcion: callback 
Descripcion: Funcion a la cual se llama por algun evento producido por el mause en la figura 1
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def callback ( event , x , y , flags , param):
    global cant_puntos, img_mod
    if event == cv2.EVENT_LBUTTONDOWN:                                     #Si el boton izquierdo se presiona
        if cant_puntos<4:
            cv2.circle(img_mod, (x,y) , 3 , (0,0,255) , -1)                    #Dibujo punto
            puntos[cant_puntos][0]=x                                       #Almaceno la posicion x del punto
            puntos[cant_puntos][1]=y                                       #Almaceno la posicion y del punto
            cant_puntos=cant_puntos+1
    elif event == cv2.EVENT_LBUTTONUP:                                     #Si el boton izquierdo fue levantado
        if cant_puntos == 4:
            cant_puntos=5                                                  #Valorizo en 5 para que cualquier click izquierdo no tenga efecto
            transformacion()
    cv2.imshow('Original', img_mod)                                 #Muestro imagen en la ventana
    
'''/*========================================================================
Funcion: callback2 
Descripcion: Funcion a la cual se llama por algun evento producido por el mause en la figura 2
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def callback2 ( event , x , y , flags , param):
    global ix , iy, fx , fy , drawing , mode, img_transformada, img_transformada_mod
    if event == cv2.EVENT_LBUTTONDOWN:                                     #Si el boton izquierdo se presiona
        drawing = True                                                     #Indico que estoy dibujando
        ix , iy = x , y                                                    #Guardo coordenadas iniciales x e y
        img_transformada_mod=copy.deepcopy(img_transformada)               #Copio la imagen orginial para borrar la anterior linea
        cv2.imshow('Resultado', img_transformada_mod)                      #Refresco la imagen
    elif event == cv2.EVENT_MOUSEMOVE:                                     #Si el mause se mueve
        if drawing is True :
            if mode is True :
                img_transformada_mod=copy.deepcopy(img_transformada)       #Copio la imagen orginial para borrar la anterior linea
                cv2.line(img_transformada_mod,(ix,iy) , (x,y) , (0,255,0) , 2) #Dibujo linea
                cv2.imshow('Resultado', img_transformada_mod)              #Refresco la imagen
            else:
                cv2.circle(img_transformada_mod, (x,y) , 5 , (0,0,255) , -1)
                cv2.imshow('Resultado', img_transformada_mod)              #Refresco la imagen
    elif event == cv2.EVENT_LBUTTONUP:                                     #Si el boton izquierdo fue levantado
        drawing = False                                                    #Indico que deje de dibujar
        if mode is True :
            tangle=cv2.line (img_transformada_mod, (ix,iy) , (x,y) , (0,255,0) , 2)  #Dibujo linea
            fx , fy = x , y                                                #Guardo posicion x e y
            distancia = math.sqrt((int(fx)-int(ix))*(int(fx)-int(ix))+(int(fy)-int(iy))*(int(fy)-int(iy)))/mts_to_pixel.get()                                             
            cv2.putText(tangle,str(round(distancia, 2))+" Mts",(ix,iy+21), cv2.FONT_HERSHEY_SIMPLEX, 0.5,( 0,0,255),1,cv2.LINE_AA)
            cv2.imshow('Resultado', img_transformada_mod)              #Refresco la imagen
        else:
            cv2.circle(img_transformada_mod, (x,y) , 5 , (0,0,255) , -1)   #Dibujo punto
            cv2.imshow('Resultado', img_transformada_mod)              #Refresco la imagen
    #cv2.imshow('Resultado', img_transformada_mod)                          #Refresco muestra de imagen con recuadro
    


'''/*========================================================================
Funcion: Abrir_foto
Descripcion: Permite seleccionar una foto
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Abrir_foto():
    global ubicacion, img, cant_puntos, img_mod                 #Obtengo las variables globales
    ubicacion = filedialog.askopenfilename(title='Abrir archivo',initialdir='/', filetypes=(('Archivo png', '*.png*'),('Archivo jpg', '*.jpg'))) #Obtengo la ruta seleccionada
    img = cv2.imread(ubicacion , cv2.IMREAD_COLOR)              #Obtengo la imagen de la ubicacion seleccionada
                                                                #Opcional: cv2.IMREAD_COLOR (0)   cv2.IMREAD_GRAYSCALE (1) cv2.IMREAD_UNCHANGED (-1)   
    cambiar_texto_label2("Foto abierta", "green")               #Cambio texto y color del label2
    cv2.namedWindow('Original')                                 #Indico nombre de la ventana
    cv2.setMouseCallback ('Original',callback)                  #Establesco evento de mause sobre la ventana
    print("Foto abierta")                                       #Indico que termino el proceso por la consola
    img_mod=copy.deepcopy(img)                                  #Copio la imagen original en una variable
    cv2.imshow('Original', img_mod)                                 #Muestro imagen en la ventana
    cant_puntos=0                                               #Reseteo la cant de puntos cuando se abre una nueva imagen

'''/*========================================================================
Funcion: Guardar_imagen
Descripcion: Permite guardar una imagen
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Guardar_imagen():
    global img_mod                                             #Obtengo las variables globales
    directorio=filedialog.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (('Archivo png', '.png'),('Archivo jpg', '.jpg'),("todos los archivos","*.*")),defaultextension='.png')  #Abro ventana para seleccionar ubicacion
    print("Ubicacion imagen recotada: ")             
    print(directorio)
    cv2.imwrite( directorio, img_mod)                           #Guardo la imagen binaria o procesada
    #showinfo.showinfo("Practico2", "Guardado con exito")       # título, mensaje
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
puerta_alto = DoubleVar()
puerta_ancho = DoubleVar()
mts_to_pixel =DoubleVar()
puerta_alto.set(2.1)
puerta_ancho.set(0.73)
mts_to_pixel.set(100)
bit = root.iconbitmap('icon.ico')
root.title(Nombre_app)
root.resizable(False, False)
root.geometry('300x380')


#Describo boton abrir archivo
open_button = ttk.Button(
    root,
    text='Abrir foto',
    command= Abrir_foto
)

#Describo boton para guardar recorte
guardar_button = ttk.Button(
    root,
    text='Guardar imagen',
    command=Guardar_imagen 
)



#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
guardar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


s2 = tk.Scale(root, variable = puerta_alto, from_=0, to=5, tickinterval=20, resolution =   0.1, orient=tk.HORIZONTAL, length=300, label = "Alto puerta [m]: ").pack()
s3 = tk.Scale(root, variable = puerta_ancho, from_=0, to=5, tickinterval=20, resolution =   0.1, orient=tk.HORIZONTAL, length=300, label = "Ancho puerta [m]: ").pack()
s4 = tk.Scale(root, variable = mts_to_pixel, from_=0, to=500, tickinterval=20,  resolution =  1, orient=tk.HORIZONTAL, length=300, label = "Relacion pixel/mts: ").pack()


#genero un label
label1 = Label(root,text="Para resetear, vuelva a cargar una imagen")
label1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.bind('<Key>', lambda i : Keyboardpress(i))                        #Indico eventos de teclado y la funcion a la que se debe llamar
root.mainloop()
