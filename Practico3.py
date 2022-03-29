'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 28/03/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 * Descripcion: Visualizacion de un video convirtiendolo a escala de grices
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk                            #Para ventana grafico
from tkinter import ttk                         #Para ventana grafico
from tkinter import *                           #Para ventana grafico
from tkinter import filedialog as filedialog    #Para abrir y guardar archivos 
import cv2                                      #Librerira opencv

#======================== Variable ====================================
ubicacion=""

#======================== Implementaciones=============================


'''/*========================================================================
Funcion: Seleccionar_video
Descripcion: Permite seleccionar el video a visualizar
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Seleccionar_video():
    global ubicacion                                             #Obtengo las variables globales
    ubicacion = filedialog.askopenfilename(title='Abrir archivo',initialdir='/', filetypes=(('Archivo mp4', '*.mp4*'),('Archivo avi', '*.avi'))) #Obtengo la ruta seleccionada
    cambiar_texto_label2("Video seleccionado", "green")          #Cambio texto y color del label2
    print("Video seleccionado")                                  #Indico que termino el proceso por la consola


'''/*========================================================================
Funcion: Reproducir_video
Descripcion: Permite reproducir el video
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Reproducir_video():
    global ubicacion                                                #Variable global
    cap = cv2.VideoCapture(ubicacion)                               #Capturo el video
    framerate = cap.get(cv2.CAP_PROP_FPS)                           #Obtengo el frame rate del video
    while (cap.isOpened()):                                         #Mientras el video continue
        ret , frame = cap.read()                                    #Leo cada frame
        gray = cv2.cvtColor ( frame , cv2.COLOR_BGR2GRAY)           #Convierto el frame en escala de grices
        cv2.imshow('frame gray', gray)                              #Muestro el frame en escala de grices
        cv2.imshow('frame original', frame)                          #Muestro el frame original
        if((cv2.waitKey(int(framerate)) & 0xFF ) == ord ('q')):     #Espero un tiempo igual a un framerate para actualizar la imagen o hasta que se precione la letra 'q'
            break

    cap.release()                                                   #Libero el video
    cambiar_texto_label2("Fin del video", "green")                  #Cambio texto y color del label2

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
root.title('Practico3')
root.resizable(False, False)
root.geometry('300x100')
barra = DoubleVar()

#Describo boton abrir archivo
open_button = ttk.Button(
    root,
    text='Seleccionar video',
    command= Seleccionar_video
)

#Describo boton para reproducir video
reproducir_button = ttk.Button(
    root,
    text='Reproducir video',
    command=lambda:[cambiar_texto_label2("Reproduciendo, por favor espere...", "red"), Reproducir_video()]
    
)

#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
reproducir_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
#genero un label
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.mainloop()