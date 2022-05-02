'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 02/05/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 *          Desarrollado en: Windows 10 x64
 *
 * Descripcion: Permite detectar un marcador aruco y calcular la distancia 3d desde
 *              el punto del centro de la camara y el punto del centro del marcadro.
 *
 *             Para esto se necesita calibrar la camara con un "tablero de ajedres"
 *             para obtener la matriz de calibracion y el vector de distorcion.
 *
 *             Este software permite hacer todo lo necesario para obtener la distancia.
 *                 1) Calibrar la camara y obtener la matriz y el vector
 *                 2) Generar un marcado aruco.
 *                 3) Medir la distancia.
 *             
 *             La matriz se puede dejar fija cambiando las variables mtx y dist.
 *             Si estas variables no se modificaron, es necesario calibrar con el proceso
 *             de captura 5 fotos mediante este software precionando el boton "Calibrar camara"
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk                            #Para ventana grafico
from tkinter import ttk                         #Para ventana grafico
from tkinter import *                           #Para ventana grafico
from tkinter import filedialog as filedialog    #Para abrir y guardar archivos
import numpy as np                              #Para tratar con numeros matematicos para opencv    
import cv2                                      #Librerira opencv
import copy                                     #Para poder copiar matrices
import glob                                     #Para buscar archivos de una misma extencion en una carpeta
from math import sin, cos, sqrt, atan2, pi      #Para aplicaciones matematicas y trigonometricas
from tkinter import messagebox                  #Para mensajes del sistema
import os                                       #Para verificar si existen rutas o archivos

#======================== Variable ====================================
Nombre_app="Practico 11 - Burgos"
mtx= np.zeros((3, 3))                           #Matriz de la camara
dist= None                                      #Distorcion de la camara
markerSizeInCM = 11.0                           #Tamaño real del marcador
cap = cv2.VideoCapture(0)                       #Capturo video del dispositivo 0

if cap.isOpened():                                              #Si hay una captura
    ret2, frame2 = cap.read()                                   #Tomo frame
    FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))        #Obtengo tamaño en x
    FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))      #Obtengo tamaño en y

#======================== Implementaciones=============================

'''/*========================================================================
Funcion: Tomar_foto
Descripcion: Permite capturar un frame desde la camara cuando se presiona una
             determinada letra y guardar dicho frame como una imagen png.
Sin parametro de entrada
Retorna:     letra:  letra que se debe precionar para capturar el frame.
             dirccion_guarado: direccion donde se guardara la imagen.
========================================================================*/'''
def Tomar_foto(letra, dirccion_guarado):
    global cap                                                                       #Variable globales
    while(cap.isOpened()):                                                           #Mientras hay captura
        ret, frame = cap.read()                                                      #Tomo frame de la camara
        if ret is True:
            cv2.imshow('Frame', frame)                                               #Muestro frame
            if cv2.waitKey(1)&0xFF==ord(letra):                                        #Si se presiona la tecla
                cv2.imwrite(dirccion_guarado,frame)                                  #Guardo imagen
                cv2.destroyWindow('Frame')                                           #Cierro frame camara
                break                                                                #Salgo del while
        else:
            break
            
'''/*========================================================================
Funcion: Calibrar_camara
Descripcion: Sirve para calibrar la camara obteninedo la matriz de la camara y la distorion
             Para esto se utilizan una serie de fotos de un tablero de ajedres tomadas en
             diferentes perspectivas con la camara que se va a utilizar (el soft indica las instrucciones).
             Si las imagenes ya existen por que se calibro anteriormente, se pueden utilizar esas mismas
             en caso contrario, el software le permite capturar las 5 imagenes mediante indicaciones prsionando
             la tecla c.
             Por ultimo se procesa la imagen y se obtiene la calibracion.
Sin parametro de entrada
Retorna:     mtx:  Matriz de calibracion de la camara.
             dist: Vector de distorcion de la camara.
========================================================================*/'''
def Calibrar_camara():
    global mtx, dist, FRAME_WIDTH, FRAME_HEIGHT                                       #Variables gloabales

    """Declaro variables que se van a utilizar"""
    tablero =(9,6)                                                                    #Esquinas internas horizontal y vertical respectivamente (del tablero de ajedres)
    tam_frame = (FRAME_WIDTH, FRAME_HEIGHT)                                           #Resolucion del frame de la camara

    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)        #Criterio con el que opencv detecta las esquinas
    
    puntos_obj = np.zeros((tablero[0]*tablero[1], 3), np.float32)                     #Preparamos los puntos del tablero
    puntos_obj[:,:2] = np.mgrid[0: tablero[0], 0:tablero[1]].T.reshape(-1,2)          #Preparamos los puntos del tablero

    puntos_3d = []                                                                    #Preparamos las listas para almacenar los puntos del mundo real y de la imagen
    puntos_img = []                                                                   #Preparamos las listas para almacenar los puntos del mundo real y de la imagen

    """Saco 5 imagenes al tablero de ajedres en diferentes angulos"""
    existe=os.path.exists('calibracion/cali0.png') and os.path.exists('calibracion/cali1.png') and os.path.exists('calibracion/cali2.png') and os.path.exists('calibracion/cali3.png') and os.path.exists('calibracion/cali4.png') #Verifico si ya existen las imagenes de calibración
    respuesta=False                                                               #Para determinar si se quieren volver a tomar las fotos para calibrar camara
    if existe == True:                                                            #Si las imagenes ya existen
        respuesta=messagebox.askokcancel(message="Ya existen imagenes para realizar la calibracion ¿Desea realizar nuevas imagenes?", title="Calibración")
    
    if (existe == True and respuesta == True) or existe == False:                 #Si las imagenes existen y se quiere tomar nuevas imagenes o si no existen
        pregunta=messagebox.askokcancel(message="En este proseso se pedira sacar 5 fotos con las instrucciones indicadas, para sacar cada foto debe presionar la letra 'c' ¿Desea continuar?", title="Calibración") #Indico procesamiento y pido confirmación

        if pregunta == False:                                                     #Si se cancelo el proceso
            return 0,0                                                            #Retorno y salgo de la funcion
        else:                                                                     #Inicio proceso para sacar fotos y guardarlas
            cambiar_texto_label2("Posiciones el tablero de forma recta y precione 'c'", "Red") #Cambio texto y color de label2
            Tomar_foto("c", "calibracion/cali0.png")                                           #Espero letra y guardo foto                                              #Reseteo variable letra
            cambiar_texto_label2("Rote el tablero a 90° y precione 'c'", "Red")                #Cambio texto y color de label2
            Tomar_foto("c", "calibracion/cali1.png")                                           #Espero letra y guardo foto 
            cambiar_texto_label2("Incline el tablero en perspectiva y precione 'c'", "Red")    #Cambio texto y color de label2
            Tomar_foto("c", "calibracion/cali2.png")                                           #Espero letra y guardo foto 
            cambiar_texto_label2("Cambie perspectiva y precione 'c'", "Red")                   #Cambio texto y color de label2
            Tomar_foto("c", "calibracion/cali3.png")                                           #Espero letra y guardo foto 
            cambiar_texto_label2("Rote el tablero y precione 'c'", "Red")                      #Cambio texto y color de label2
            Tomar_foto("c", "calibracion/cali4.png")                                           #Espero letra y guardo foto 
            
    else:
        print("Utilizando imagenes existentes")

    """Realizo el proceso de calibracion con las 5 imagenes"""
    fotos = glob.glob('calibracion/*.png')                                            #Busco los archivos con formato .png en el directorio indicado
    for foto in fotos:                                                                #Recorro cada archivo .png encontrado
        #print(foto)
        img = cv2.imread(foto)                                                        #Leo la imagen
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                  #Convierto a escala de grises

        ret, esquinas =cv2.findChessboardCorners(gray, tablero, None)                 #Buscamos las esquinas del tablero

        if ret == True:
            puntos_3d.append(puntos_obj)                                              #Agrego a puntos_3d los puntos_obj          
            esquinas2 = cv2.cornerSubPix(gray, esquinas, (11,11), (-1,-1), criterio)  #Encuentra la ubicación precisa de subpíxeles de las esquinas
            puntos_img.append(esquinas)                                               #Agrego esquinas a puntos_img
            cv2.drawChessboardCorners(img, tablero, esquinas2, ret)                   #Dibujo las esquinas del tablero en el frame
            cv2.imshow("img calibracion", img)                                        #Muestro frame con las esquinas encontradas

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(puntos_3d, puntos_img, tam_frame, None, None) #Calibracion de la camara
    print ("Matriz de calibración:")
    print (mtx)
    print ("Vector de distorción:")
    print (dist)
    cambiar_texto_label2("Calibracion exitosa", "Green")                              #Cambio texto y color de label2
    return mtx, dist

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
Funcion: Medir_distancia
Descripcion: Introduce los videos con realidad virtual entre el rectangulo que
             generan los marcadores 0, 1, 2, 3 (en sentido horario) mediante
             rectificacion de la imagen de cada frame.
             Tambien se usan los marcadores 4,5,6 para avanzar video hacia delante
             hacia atras y mute respectivamente.
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Medir_distancia():
    global mtx, dist, markerSizeInCM

    if (mtx == np.zeros((3, 3))).all():            #Si la camra no esta calibrada
        messagebox.showerror(message="Es necesario calibrar la camara primero", title="Error")
        return                                                          #Salgo de la funcion

    if (dist == None).all():                                            #Si la camra no esta calibrada
        messagebox.showerror(message="Es necesario calibrar la camara primero", title="Error")
        return                                                          #Salgo de la funcion
        
    cambiar_texto_label2("Para salir presione la letra 'q'", "black")   #Cambio texto y color de label2
    
    while(cap.isOpened()):                                                     #Mientras hay captura
        ret, frame = cap.read()                                                #Tomo frame de la camara
        if ret is True:                                             
            dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)      #Cargo el diccionario que se utilizó para generar los marcadores.
            parameters =  cv2.aruco.DetectorParameters_create()                #Inicializo los parámetros del detector utilizando los valores predeterminados
            markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters) #Detecto los marcadores en el frame de la camara
            #print("Cant: "+str(len(markerCorners)))
            #print(np.array(markerIds))
            
            if (np.array(markerIds) != None).all():                                     #Si existe marcadores en el frame
                if (0 in markerIds):                                                    #Si existe marcador con id 0
                    esquinas=obtener_puntos_marcador(0, markerCorners, markerIds)       #Obtengo esquinas del marcador 4
                    imagen = cv2.imread('recursos/Punto_medicion.png')                  #Leo la imagen de flecha arriba
                    frame=transformacion(esquinas[0], esquinas[1], esquinas[2], esquinas[3], frame, imagen) #Realizo la transformacion incustando una imagen en el marcado 0
                    
                    rvec , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(markerCorners, markerSizeInCM, mtx, dist) #Obtengo el vector de rotacion y desplazamiento de la camara respecto al centro del marcador aruco indicando las esquinas y el tamaño del marcador como tambien la matriz de calibracion de la camara y su distorcion (obtenidas de la calibración)
                   
                    #frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
                    frame =cv2.aruco.drawAxis(frame, mtx, dist, rvec, tvec, 0.178)      #Dibujos los ejes cartecianos
                    
                    #rvec entrega la distancia entre el punto de la camara y el centro del marcador aruco, por lo tanto entrega un vector que contiene la distancia x, y, z entre los dos puntos
                    #rcev esta compuesto por tvec[a][b][c] donde a es el id del marcador, b debe ser 0, c es la posicion para obtener la distancia x, y, z
                    inclinacion_rad = -1 * atan2(tvec[0][0][0], tvec[0][0][2])          #Trigonometria para obtener el angulo  https://www.superprof.es/apuntes/escolar/matematicas/analitica/recta/angulo-que-forman-dos-rectas.html
                    inclinacion = inclinacion_rad / pi * 180                            #Convierto de rad a grados
                    zDist = sqrt(tvec[0][0][0] ** 2 + tvec[0][0][1] ** 2 + tvec[0][0][2] ** 2)  #Trigonometria para encontrar la distancia en 3D (Modulo del vector) https://www.geogebra.org/m/QjnTG76X
                    
                    #print(str(zDist)+" cm "+str(inclinacion)+" °")
                    cv2.putText(frame, "%.2f cm  %.2f deg" % (zDist, inclinacion), (esquinas[3][0]+1, esquinas[3][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0)) #Escribo la distancia y angulo en el marcador
                    
            cv2.imshow('Salida', frame)                                                 #Muestro el frame final
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

#Describo boton para calibrar camara
Calibrar_camara_bt = ttk.Button(
    root,
    text='Calibrar camara',
    command=Calibrar_camara
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
    text='Medir distancia',
    command=Medir_distancia
)


#Implemento los botones en el root
Calibrar_camara_bt.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
s1 = tk.Scale(root, variable = id_generar, from_=0, to=100, tickinterval=20,  resolution =  1, orient=tk.HORIZONTAL, length=300, label = "Id del marcador a generar: ").pack()
Generar_marcador.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
Reproducir_video.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

#genero un label
label1 = Label(root,text="")
label1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.mainloop()
