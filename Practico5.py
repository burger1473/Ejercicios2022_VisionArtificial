'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 28/03/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 * Descripcion: Recortador de imagen
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk                            #Para ventana grafico
from tkinter import ttk                         #Para ventana grafico
from tkinter import *                           #Para ventana grafico
from tkinter import filedialog as filedialog    #Para abrir y guardar archivos
import numpy as np                              #Para tratar con numeros matematicos para opencv    
import cv2                                      #Librerira opencv
import copy                                     #Para poder copiar matrices

#======================== Variable ====================================
ubicacion=""
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press ’m’ to toggle to curve
ix= -1
iy= -1
fx= -1
fy= -1
img = np.zeros((512, 512, 3),np.uint8)
img_mod = np.zeros((512, 512, 3),np.uint8)
img_rec = np.zeros((1, 1, 3),np.uint8)
imagen_visible = 0

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
    if key_char == 'r':
        Reset()
    if key_char == 'g':
        Guardar_recorte()
    if key_char == 'q':
        cv2.destroyAllWindows()     #Cierro las ventans de opencv
        root.destroy()              #Destruyo la aplicacion 


'''/*========================================================================
Funcion: draw_paint 
Descripcion: Funcion a la cual se llama por algun evento producido por el mause
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def draw_paint ( event , x , y , flags , param):
    global ix , iy, fx , fy , drawing , mode, img_mod, img_rec, imagen_visible
    if event == cv2.EVENT_LBUTTONDOWN:                                     #Si el boton izquierdo se presiona
        drawing = True                                                     #Indico que estoy dibujando
        ix , iy = x , y                                                    #Guardo coordenadas iniciales x e y
        img_mod=copy.deepcopy(img)                                         #Copio la imagen orginial para borrar el anterior recuadro verde
        cv2.imshow('image', img_mod)                                       #Refresco la imagen
    elif event == cv2.EVENT_MOUSEMOVE:                                     #Si el mause se mueve
        if drawing is True :
            if mode is True :
                img_mod=copy.deepcopy(img)                                 #Copio la imagen orginial para borrar el anterior recuadro verde
                cv2.imshow('image', img_mod)                               #Refresco la imagen
                cv2.rectangle(img_mod,(ix,iy) , (x,y) , (0,255,0) , -1)    #Dibujo rectangulo
            else:
                cv2.circle(img_mod , (x,y) , 5 , (0,0,255) , -1)
    elif event == cv2.EVENT_LBUTTONUP:                                     #Si el boton izquierdo fue levantado
        drawing = False                                                    #Indico que deje de dibujar
        if mode is True :
            cv2.rectangle (img_mod, (ix,iy) , (x,y) , (0,255,0) , -1)      #Dibujo rectangulo
            fx , fy = x , y                                                #Guardo posicion x e y
            img_rec=img[iy:fy, ix:fx]                                      #Recorto imagen
            img_mod=copy.deepcopy(img)                                     #Copio la imagen orginial para borrar el anterior recuadro verde
            cv2.imshow('image', img_mod)                                   #Refresco la imagen
            if imagen_visible:
                cv2.destroyWindow('Recorte')                               #Cierro la ventana anterior del recorte
            cv2.imshow('Recorte', img_rec)                                 #Refresco muestra de imagen recortada
            imagen_visible = 1                                             #Indico que la ventana esta abierta para luego cerrarla antes de refrescar un nuevo recorte
        else:
            cv2.circle(img_mod, (x,y) , 5 , (0,0,255) , -1)                #Dibujo punto
    cv2.imshow('image', img_mod)                                           #Refresco muestra de imagen con recuadro
    
    
    
'''/*========================================================================
Funcion: Abrir_foto
Descripcion: Permite seleccionar una foto
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Abrir_foto():
    global ubicacion, img, img_mod                              #Obtengo las variables globales
    ubicacion = filedialog.askopenfilename(title='Abrir archivo',initialdir='/', filetypes=(('Archivo png', '*.png*'),('Archivo jpg', '*.jpg'))) #Obtengo la ruta seleccionada
    img = cv2.imread(ubicacion , cv2.IMREAD_COLOR)              #Obtengo la imagen de la ubicacion seleccionada
                                                                #Opcional: cv2.IMREAD_COLOR (0)   cv2.IMREAD_GRAYSCALE (1) cv2.IMREAD_UNCHANGED (-1)   
    cambiar_texto_label2("Foto abierta", "green")               #Cambio texto y color del label2
    cv2.namedWindow('image')                                    #Indico nombre de la ventana
    cv2.setMouseCallback ('image',draw_paint)                   #Establesco evento de mause sobre la ventana
    print("Foto abierta")                                       #Indico que termino el proceso por la consola
    cv2.imshow('image', img)                                    #Muestro imagen en la ventana
    img_mod=copy.deepcopy(img)                                  #Copio la imagen original en una variable


'''/*========================================================================
Funcion: Guardar_recorte
Descripcion: Permite guardar una imagen
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Guardar_recorte():
    global img_rec                                              #Obtengo las variables globales
    directorio=filedialog.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (('Archivo png', '.png'),('Archivo jpg', '.jpg'),("todos los archivos","*.*")),defaultextension='.png')  #Abro ventana para seleccionar ubicacion
    print("Ubicacion imagen recotada: ")             
    print(directorio)
    cv2.imwrite( directorio, img_rec)                           #Guardo la imagen binaria o procesada
    #showinfo.showinfo("Practico2", "Guardado con exito")       # título, mensaje
    cambiar_texto_label2("Guardado con exito", "black")         #Cambio texto y color de label2


'''/*========================================================================
Funcion: Reset
Descripcion: Permite resetear el recorte
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Reset():
    global img, img_mod                                        #Obtengo las variables globales
    img_mod=copy.deepcopy(img)                                 #Copio imagen original en img_mod
    cv2.imshow('image', img_mod)                               #Restauro la vista de la imagen a recortar
    

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

bit = root.iconbitmap('icon.ico')
root.title('Practico 5 - Fabian Burgos')
root.resizable(False, False)
root.geometry('300x140')
barra = DoubleVar()

#Describo boton abrir archivo
open_button = ttk.Button(
    root,
    text='Abrir foto',
    command= Abrir_foto
)

#Describo boton para guardar recorte
guardar_button = ttk.Button(
    root,
    text='Guardar recorte',
    command=Guardar_recorte 
)

#Describo boton para resetear recorte
reset_button = ttk.Button(
    root,
    text='Reset',
    command=Reset 
)

#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
guardar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
reset_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
#genero un label
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.bind('<Key>', lambda i : Keyboardpress(i))                        #Indico eventos de teclado y la funcion a la que se debe llamar
root.mainloop()
