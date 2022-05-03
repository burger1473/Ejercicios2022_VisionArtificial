'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 27/04/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 *          Desarrollado en: Windows 10 x64
 * Descripcion: Deteccion de 6 marcadores ARuCo y visualización de videos seleccionados
 *              sobre las 4 esquinas de los primeros 4 marcadores. Los otros dos marcadores
 *              se utilizan para cambiar los videos hacia adelante o hacia atras como en un tv.
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
Nombre_app="Practico 11 - Burgos"
ubicacion=""
cap = cv2.VideoCapture(0)                                       #Capturo video del dispositivo 0
n_video=0

#======================== Implementaciones=============================

'''/*========================================================================
Funcion: transformación
Descripcion: Realiza el rectificado de una imagen y la incrusta en otra
Parametro de entrada:
                     pto0: array con cordenada 'x' e 'y' del punto superior izquiero del recuadro donde se debe incrustar la imagen
                     pto1: array con cordenada 'x' e 'y' del punto superior derecho del recuadro donde se debe incrustar la imagen
                     pto2: array con cordenada 'x' e 'y' del punto inferior derecho del recuadro donde se debe incrustar la imagen
                     pto3: array con cordenada 'x' e 'y' del punto inferior izquiero del recuadro donde se debe incrustar la imagen
                     img1: imagen original donde se debe inscrustar la transformada de la otra imagen
                     img2: imagen a transformar e incrustar en la imagen original
Retorna:             Retorna la imagen final procesada con la segunda imagen ya incrustada
========================================================================*/'''
def transformacion(pto0, pto1, pto2, pto3, img1, img2):
    
    rows, cols = img2.shape[:2]                               #Tamaño de la imagen a transformar e incrustar
    rows2, cols2 = img1.shape[:2]                             #Tamaño de la imagen original

    #Defino los 4 pares de puntos correspondientes
    input_pts = np.float32([[0,0], [cols,0], [cols,rows], [0,rows]])
    output_pts = np.float32([[pto0[0],pto0[1]], [pto1[0],pto1[1]], [pto2[0],pto2[1]], [pto3[0],pto3[1]]])
   
    M = cv2.getPerspectiveTransform(input_pts , output_pts)   #Calcule la matriz de transformación usando cv2.getPerspectiveTransfor()
    #M, status = cv2.findHomography(input_pts , output_pts)
    
    Perspectiva = cv2.warpPerspective(img2, M, (cols2,rows2)) #Aplico la transformación afín usando cv2.warpAffine()
    cv2.fillConvexPoly(img1, output_pts.astype(int), 8, 16)   #se puede usar para llenar un polígono convexo, solo proporcione los vértices del polígono convexo.
                                                              #Rellana con blanco el poligono formado por los puntos de salida
    img1=img1+Perspectiva                                     #Sumo la imagen original con la perspectiva
    #cv2.imshow('Resultado', img1)                            #Muestro el resultado
    return img1
    
'''/*========================================================================
Funcion: Seleccionar_videos
Descripcion: Permite seleccionar multiples videos que se van a mostrar
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Seleccionar_videos():
    global ubicacion                                            #Obtengo las variables globales
    ubicacion = filedialog.askopenfilename(title='Abrir archivos',initialdir='/', filetypes=(('Archivo mp4', '*.mp4*'),('Archivo avi', '*.avi')), multiple=True) #Obtengo la ruta seleccionada
    cambiar_texto_label2("Videos seleccionados", "green")       #Cambio texto y color del label2

'''/*========================================================================
Funcion: Generar_Aruco
Descripcion: Permite generar un marcador aruco y guardarlo en una imagen
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Generar_Aruco():
    global id_generar
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250) #Cargo el diccionario predefinido
    markerImage = np.zeros((200, 200), dtype=np.uint8)            #Genero el marcador
    markerImage = cv2.aruco.drawMarker(dictionary, int(id_generar.get()), 200, markerImage, 1);
    cv2.imshow("marcador"+str(int(id_generar.get())), markerImage);
    directorio=filedialog.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (('Archivo png', '.png'),('Archivo jpg', '.jpg'),("todos los archivos","*.*")),defaultextension='.png')  #Abro ventana para seleccionar ubicacion
    print("Ubicacion imagen guardada: ")             
    print(directorio)
    cv2.imwrite( directorio, markerImage)                         #Guardo la imagen
    cambiar_texto_label2("Guardado con exito", "black")           #Cambio texto y color de label2

'''/*========================================================================
Funcion: obtener_puntos_marcador
Descripcion: Obtiene las esquinas de un marcador aruco
Parametro entrada: id: numero id del marcador al cual se quiere obtener las esquinas
                   markerCorners: esquinas de cada marcador (se obtiene previamente con cv2.aruco.detectMarkers)
                   markerIds: ids de todos los marcadores que existen (se obtiene previamente con cv2.aruco.detectMarkers)
Retorna un array con las 4 esquinas
========================================================================*/'''
def obtener_puntos_marcador(id, markerCorners, markerIds):
    index = np.squeeze(np.where(markerIds==id))                  #Obtiene la posicion del id x en el array
    refPt0 = np.squeeze(markerCorners[index[0]])[0]              #Obtiene la esquina 0 del id de index
    refPt1 = np.squeeze(markerCorners[index[0]])[1]              #Obtiene la esquina 1 del id de index
    refPt2 = np.squeeze(markerCorners[index[0]])[2]              #Obtiene la esquina 2 del id de index
    refPt3 = np.squeeze(markerCorners[index[0]])[3]              #Obtiene la esquina 3 del id de index
    esquinas=np.array([
                        [int(refPt0[0]), int(refPt0[1])], 
                        [int(refPt1[0]), int(refPt1[1])],
                        [int(refPt2[0]), int(refPt2[1])],
                        [int(refPt3[0]), int(refPt3[1])]
                      ], np.int32)
    return esquinas

'''/*========================================================================
Funcion: Video_RA
Descripcion: Introduce los videos con realidad virtual entre el rectangulo que
             generan los marcadores 0, 1, 2, 3 (en sentido horario) mediante
             rectificacion de la imagen de cada frame.
             Tambien se usan los marcadores 4,5,6 para avanzar video hacia delante
             hacia atras y mute respectivamente.
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Video_RA():
    global n_video
    flecha_arriba=0
    flecha_abajo=0
    Num_frame=0
    cambiar_texto_label2("Para salir del RA presione la letra 'q'", "black")   #Cambio texto y color de label2
    if ubicacion == "":
        cambiar_texto_label2("Seleccione un video primero", "red")             #Cambio texto y color de label2
        return 0                                                               #Salgo de la funcion retornando cero

    cap2 = cv2.VideoCapture(ubicacion[n_video])                                #Capturo el video que se encuentra en la ubicacion en la posicion n_video
    framerate = cap2.get(cv2.CAP_PROP_FPS)                                     #Obtengo el frame rate del video
    while(cap.isOpened()):                                                     #Mientras hay captura
        ret, frame = cap.read()                                                #Tomo frame de la camara
        if ret is True:                                             
            dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)      #Cargo el diccionario que se utilizó para generar los marcadores.
            parameters =  cv2.aruco.DetectorParameters_create()                #Inicializo los parámetros del detector utilizando los valores predeterminados
            markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters) #Detecto los marcadores en el frame de la camara
            #print("Cant: "+str(len(markerCorners)))
            #print(np.array(markerIds))
            
            if (np.array(markerIds) != None).all():                            #Si existe marcadores en el frame
                if (0 in markerIds) and (1 in markerIds) and (2 in markerIds) and (3 in markerIds): #Si estan los marcadores del 0 al 3
                    index_id0 = np.squeeze(np.where(markerIds==0))             #Obtiene la posicion del id x en el array
                    refPt0_id0 = np.squeeze(markerCorners[index_id0[0]])[0]    #Obtiene la esquina 0 del id de index

                    index_id1 = np.squeeze(np.where(markerIds==1))             #Obtiene la posicion del id x en el array
                    refPt1_id1 = np.squeeze(markerCorners[index_id1[0]])[1]    #Obtiene la esquina 1 del id de index

                    index_id2 = np.squeeze(np.where(markerIds==2))             #Obtiene la posicion del id x en el array
                    refPt2_id2 = np.squeeze(markerCorners[index_id2[0]])[2]    #Obtiene la esquina 2 del id de index

                    index_id3 = np.squeeze(np.where(markerIds==3))             #Obtiene la posicion del id x en el array
                    refPt3_id3 = np.squeeze(markerCorners[index_id3[0]])[3]    #Obtiene la esquina 2 del id de index

                    retvid , framevid = cap2.read()                            #Leo cada frame del video a mostrar
                    
                    frame=transformacion(refPt0_id0, refPt1_id1, refPt2_id2, refPt3_id3, frame, framevid) #Realizo la transformacion
                    #cv2.rectangle(frame,(int(refPt0_id0[0]),int(refPt0_id0[1])) , (int(refPt2_id2[0]),int(refPt2_id2[1])) , (0,255,0) , -1)    #Dibujo rectangulo    
                    
                    if (4 in markerIds):                                                #Si existe marcador 4
                        esquinas=obtener_puntos_marcador(4, markerCorners, markerIds)   #Obtengo esquinas del marcador 4
                        imagen = cv2.imread('recursos/flecha_arriba.jpg')               #Leo la imagen de flecha arriba
                        frame=transformacion(esquinas[0], esquinas[1], esquinas[2], esquinas[3], frame, imagen) #Realizo la transformacion incustando la flecha en el marcado 4
                        flecha_arriba=1                                                 #Indico que se coloco la flecha y que el marcador 4 esta siendo detectado
                    else:                                                               #Si no detecto el marcador 4
                        if flecha_arriba == 1:                                          #Si anteriormente se estaba detectando el marcador 4
                            n_video=n_video+1                                           #Cambio de video (ya que se presiono la flecha provocando que el marcador se deje de detectar por un tiempo corto)
                            flecha_arriba=0                                             #Indico que el marcador 4 no se detecto

                    if (5 in markerIds):                                                #Si existe marcador 5
                        esquinas=obtener_puntos_marcador(5, markerCorners, markerIds)   #Obtengo esquinas del marcador 5
                        imagen = cv2.imread('recursos/flecha_abajo.jpg')                #Leo la imagen de flecha abajo
                        frame=transformacion(esquinas[0], esquinas[1], esquinas[2], esquinas[3], frame, imagen) #Realizo la transformacion incustando la flecha en el marcado 5
                        flecha_abajo=1                                                  #Indico que se coloco la flecha y que el marcador 5 esta siendo detectado
                    else:                                                               #Si no detecto el marcador 5
                        if flecha_abajo == 1:                                           #Si anteriormente se estaba detectando el marcador 5
                            n_video=n_video-1                                           #Cambio de video (ya que se presiono la flecha provocando que el marcador se deje de detectar por un tiempo corto)
                            flecha_abajo=0                                              #Indico que el marcador 5 no se detecto
                    
                    if flecha_abajo == 0 or flecha_arriba == 0:                         #Si existio un cambio de video
                        if n_video >= len(ubicacion):                                   #Si el numero incrementado es mayor a la cantidad de videos seleccionados
                            n_video = 0                                                 #Indico que el video actual es el primero ya que vuelvo al incio
                        if n_video < 0:                                                 #Si el numero decrementado es menor a cero
                            n_video = len(ubicacion)-1                                  #Indico que el video actual es el ultimo video seleccionado
                        cap2 = cv2.VideoCapture(ubicacion[n_video])                     #Cambio el video a reproducir

            cv2.imshow('Salida', frame)                                                 #Muestro el frame final
            Num_frame += 1                                                              #Incrmento por cada frame reproducido
            if Num_frame == cap2.get(cv2.CAP_PROP_FRAME_COUNT)-10:                      #Si el numero de frame es igual a la cantidad de frame que tiene el video
                Num_frame = 0                                                           #Reseteo los frame del video para que vuelva a comenzar en loop
                cap2 = cv2.VideoCapture(ubicacion[n_video])                             #Reseteo los frame del video para que vuelva a comenzar
            if cv2.waitKey(1)&0xFF==ord('q'):                                           #Si se presiona la tecla 'q'
                cv2.destroyWindow('Salida')                                             #Cierro frame camara
                break                                                                   #Salgo del while
                                
        else:                                                   
            break                                                                       #Salgo del while 
    
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
    text='Seleccionar videos',
    command= Seleccionar_videos
)

#Describo boton para generar marcador
Generar_marcador = ttk.Button(
    root,
    text='Generar marcador',
    command=Generar_Aruco 
)

#Describo boton para visualizar video por realidad aumentada
Reproducir_video = ttk.Button(
    root,
    text='Ver video en RA',
    command=Video_RA
)



#Implemento los botones en el root
open_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
s1 = tk.Scale(root, variable = id_generar, from_=0, to=100, tickinterval=20,  resolution =  1, orient=tk.HORIZONTAL, length=300, label = "Id del marcador a generar: ").pack()
Generar_marcador.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
Reproducir_video.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

#Genero un label
label1 = Label(root,text="")
label1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.mainloop()
