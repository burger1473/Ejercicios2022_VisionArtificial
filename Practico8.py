'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 18/04/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 * Descripcion: Transformación afín - Incrustando imágenes
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
Nombre_app="Practico 8"
ubicacion=""
img = np.zeros((512, 512, 3),np.uint8)
img_mod = np.zeros((512, 512, 3),np.uint8)
img_dos = np.zeros((512, 512, 3),np.uint8)
cant_puntos = 0
puntos = [[0,0],[0,0],[0,0]]

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
        Guardar_()
    if key_char == 'q':
        cv2.destroyAllWindows()     #Cierro las ventans de opencv
        root.destroy()              #Destruyo la aplicacion 


'''/*========================================================================
Funcion: transformacion_afin
Descripcion: Realiza la transformacion afin de una imagen y la incrusta en otra
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def transformacion_afin():
    global img, img_dos, img_mod
    rows, cols = img_dos.shape[:2]  #Tamaño de la imagen a transformar e incrustar
    rows2, cols2 = img.shape[:2]    #Tamaño de la imagen original

    #Defino los 3 pares de puntos correspondientes
    input_pts = np.float32([[0,0], [cols,0], [cols,rows]])
    output_pts = np.float32([[puntos[0][0],puntos[0][1]], [puntos[1][0],puntos[1][1]], [puntos[2][0],puntos[2][1]]])
    
    #Calcule la matriz de transformación usando cv2.getAffineTransform()
    M= cv2.getAffineTransform(input_pts , output_pts)
    
    #Aplico la transformación afín usando cv2.warpAffine()
    dst = cv2.warpAffine(img_dos, M, (cols2,rows2))
    
    cambiar_texto_label2("Por favor espere...", "blue")  #Cambio texto y color de label2

    #Realizo mascara e incruso la imagen
    for row in range (dst.shape[1]):                    #Recorro el ancho de la imagen transformada
        for col in range (dst.shape[0]):                #Recorro el largo de la imagen transformada
            if (dst[col][row] != 0).all():              #Si el pixel no es el color negro
                img_mod[col][row]=dst[col][row]         #Remplazo el pixel de la foto original con el pixel de la foto transformada
    
    cv2.imshow('Resultado', img_mod)                    #Muestro el resultado
    cambiar_texto_label2("Proceso finalizado", "green") #Cambio texto y color de label2


'''/*========================================================================
Funcion: callback 
Descripcion: Funcion a la cual se llama por algun evento producido por el mause
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def callback ( event , x , y , flags , param):
    global img, cant_puntos, img_dos
    if event == cv2.EVENT_LBUTTONDOWN:                                     #Si el boton izquierdo se presiona
        if cant_puntos<3:
            cv2.circle(img, (x,y) , 5 , (0,0,255) , -1)                    #Dibujo punto
            puntos[cant_puntos][0]=x                                       #Almaceno la posicion x del punto
            puntos[cant_puntos][1]=y                                       #Almaceno la posicion y del punto
            cant_puntos=cant_puntos+1
    elif event == cv2.EVENT_LBUTTONUP:                                     #Si el boton izquierdo fue levantado
        if cant_puntos == 3:
            cambiar_texto_label2("Seleccionar imagen a incrustar", "red")  #Cambio texto y color de label2
            ubicacion = filedialog.askopenfilename(title='Seleccionar imagen a incrustar',initialdir='/', filetypes=(('Archivo png', '*.png*'),('Archivo jpg', '*.jpg'))) #Obtengo la ruta seleccionada
            img_dos = cv2.imread(ubicacion , cv2.IMREAD_COLOR)             #Obtengo la imagen de la ubicacion seleccionada
            cant_puntos=4                                                  #Valorizo en 4 para que cualquier click izquierdo no tenga efecto
            transformacion_afin()

    cv2.imshow('Original', img)                                            #Refresco muestra de imagen con recuadro


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
    cv2.imshow('Original', img)                                 #Muestro imagen en la ventana
    img_mod=copy.deepcopy(img)                                  #Copio la imagen original en una variable
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

bit = root.iconbitmap('icon.ico')
root.title(Nombre_app)
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
    command=Guardar_imagen 
)



#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
guardar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

#genero un label
label1 = Label(root,text="Para resetear, vuelva a cargar una imagen")
label1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.bind('<Key>', lambda i : Keyboardpress(i))                        #Indico eventos de teclado y la funcion a la que se debe llamar
root.mainloop()
