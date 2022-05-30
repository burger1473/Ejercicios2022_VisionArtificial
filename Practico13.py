'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 30/05/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 *          TensorFlow 2.9.1
 *          Desarrollado en: Windows 10 x64
 * Descripcion: Clasificación de imágenes usando CNN
 *              Este software selecciona entre dos frutas para derivarlas en diferentes 
 *              cintas de transporte en un proceso industrial.
 *===========================================================================*/'''

#======================== Incluciones ====================================
import tkinter as tk                            #Para ventana grafico
from tkinter import ttk                         #Para ventana grafico
from tkinter import *                           #Para ventana grafico
from tkinter import filedialog as filedialog
from turtle import distance                     #Para abrir y guardar archivos
import numpy as np                              #Para tratar con numeros matematicos para opencv    
import cv2                                      #Librerira opencv
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from keras.models import load_model
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image                     #Para transformar una imagen en tensor
import matplotlib.pyplot as plt

#======================== Variable ====================================
Nombre_app="Practico 13 - Burgos"
ubicacion=""
model = Sequential()
cap = cv2.VideoCapture(0)                                           #Capturo video del dispositivo 0
#======================== Implementaciones=============================

'''/*========================================================================
Funcion: Abrir
Descripcion: Permite abrir un modelo previamente entrenado
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Abrir():
    global model                                                #Obtengo las variables globales
    ubicacion = filedialog.askdirectory()                       #Obtengo la ruta seleccionada
    model = tf.keras.models.load_model(ubicacion)               #Cargo modelo
    cambiar_texto_label2("Modelo cargado con exito", "green")   #Cambio texto y color del label2


'''/*========================================================================
Funcion: Guardar
Descripcion: Permite guardar el modelo entrenado
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Guardar():
    global model                                                #Obtengo las variables globales
    ubicacion = filedialog.askdirectory()                       #Obtengo la ruta seleccionada
    model.save(ubicacion)                                       #Guardo modelo
    cambiar_texto_label2("Guardado con exito", "black")         #Cambio texto y color de label2

'''/*========================================================================
Funcion: Ensayar
Descripcion: Permite entrenar el modelo mediante la seleccion de una carpeta que contenga las imagenes de dataset
              tambien se evalua el modelo entrenado y se testea con imagenes de pruebas que existen dentro del dataset
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Entrenar():
  cambiar_texto_label2("Entrenando modelo. Por favor espere...", "black")       #Cambio texto y color de label2
  global model
  ubicacion = filedialog.askdirectory(title='Abrir dataset')                    #Obtengo la ruta seleccionada
  #Creamos la clase que usaremos para crear los datasets. Creamos el conjunto de entrenamiento y el de test.
  train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2)#Creamos un objeto del tipo imagedatagenerator para las imagenes de entrenamiento
                                                                                         #configurando la escala, el zoom y el estiramiento de las imagenes
  test_datagen = ImageDataGenerator(rescale = 1./255)                           #Creamos un objeto del tipo imagedatagenerator para las imagenes de testero, configurando la escala

  training_set = train_datagen.flow_from_directory(ubicacion +'/train',         #Coloco las imagenes que se encuentran en la carpeta train en el objeto creado anteriormente
  target_size = (64, 64),                                                       #Cambio el tamaño a 64x64, esto se debe a que las redes neuronales tienen una x cantidad de neutronas de entradas y no se le puede ingresar una imagen de tamaño superior
  batch_size = 32,                                                              #Cuantas muestras de entrenamiento se le va a dar por cada interacion de descenso de gradiente. Mientras mayor es el numero, mayor procesamiento se necesitara en el entrenamiento.
  class_mode = 'binary')                                                        #Modelo binario para dos conjuntos de clases
                                                                                #class_mode puede ser categorical

  test_set = test_datagen.flow_from_directory(ubicacion +'/test',               #Coloco las imagenes que se encuentran en la carpeta test en el objeto creado anteriormente
  target_size = (64, 64),                                                       #Cambio el tamaño a 64x64, esto se debe a que las redes neuronales tienen una x cantidad de neutronas de entradas y no se le puede ingresar una imagen de tamaño superior
  batch_size = 32,                                                              #Cuantas muestras de entrenamiento se le va a dar por cada interacion de descenso de gradiente. Mientras mayor es el numero, mayor procesamiento se necesitara en el entrenamiento.
  class_mode = 'binary')                                                        #Modelo binario para dos conjuntos de clases

  #Creamos modelo
  model = tf.keras.models.Sequential([            
  tf.keras.layers.experimental.preprocessing.Resizing(64, 64,interpolation='bilinear'), #Cambio tamaño de las imagenes a 64x64 (no es necesario ya que se hizo en el paso anterior)                         
  tf.keras.layers.Conv2D(6, (6, 6), activation='relu', input_shape=(64, 64, 3)),        #Capa de convolucion 1                          
  tf.keras.layers.Conv2D(12, (5, 5), strides=(2, 2), activation='relu'),                #Capa de convolucion 2
  tf.keras.layers.Conv2D(24, (4, 4), strides=(2, 2), activation='relu'),                #Capa de convolucion 3
  tf.keras.layers.Flatten(),                                                            #Capa de alisado, la entrada deja de ser una matriz y pasa a ser un vector de una sola dimención
  tf.keras.layers.Dropout(rate=.25),                                                    #La capa Dropout establece aleatoriamente las unidades de entrada en 0 con una frecuencia de rate en cada paso durante el tiempo de entrenamiento, lo que ayuda a evitar el sobreajuste. Las entradas que no se establecen en 0 se escalan en 1/(1 - tasa) de modo que la suma de todas las entradas no cambia.
  tf.keras.layers.Dense(200, activation='relu'),                                        #La capa densa es la capa regular de red neuronal profundamente conectada. Es la capa más común y de uso frecuente. La capa densa realiza la siguiente operación en la entrada y devuelve la salida. output = activation(dot(input, kernel) + bias)
  tf.keras.layers.Dense(2, activation='softmax')                                        #Capa de activacion softmax para x clases (en este caso 2)
  ])                                                                              

  optimizer = tf.keras.optimizers.Adam(decay=.0001)                                     #Optimizador adam con un decaimiento de la tasa de aprendizaje

  model.compile(optimizer=optimizer,                                              
                loss='sparse_categorical_crossentropy',                           
                metrics=['accuracy'])

  #Entrenamos el modelo en el conjunto de entrenamiento
  model.fit(training_set, epochs = 25)

  #Evaluamos el modelo en el conjunto de test
  print(model.evaluate(test_set))

  #Evaluamos sobre algunas imágenes de test individuales.
  b = test_set.next()                                               #Obtengo los valores de las imagenes test
  print(b[1][0:10])                                                 #Imprimo las etiquetas verdaderas
  print(model.predict(b[0][0:10]))                                  #Calculo las probabilidades con el modelo
  cambiar_texto_label2("Modelo entrenado", "green")                 #Cambio texto y color de label2

'''/*========================================================================
Funcion: Ensayar
Descripcion: Permite ensyar el modelo previamente entrenado mediante la carga de imagenes nuevas
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Ensayar():
  ubicacion = filedialog.askopenfilename(title='Abrir imagen',initialdir='/', filetypes=(('Archivo jpg', '*.jpg'),('Archivo png', '*.png*'))) #Obtengo la ruta seleccionada
  imagen = cv2.imread(ubicacion, 1) 
  img = image.load_img(ubicacion, target_size=(64, 64))              #Cargo la imagen desde colab
  img_array = image.img_to_array(img)                                #La convierto a array
  img_batch = np.expand_dims(img_array, axis=0)                      #La convierto a tensor
  #Realizo predicion
  prediction = model.predict(img_batch)                              #Obtengo la prediccion de la imagen
  print (prediction)                                                 #Imprimo resultado
  
  if prediction[0][0] > prediction[0][1]:                            #Si la mas probable que sea de la clase 1
    if prediction[0][0] > 0.8:                                       #Si la probabilidad es mayor al 80%
      name=str(prediction[0][0]*100)+"% Manzana"                     #Indico que es una manzana
    else:                                                            #Sino
      name="No es manzana ni naranja"                                #Indico que no es manzana ni naranja
  else:                                                              #Si es mas probable que sea de la clase 2
    if prediction[0][1] > 0.8:                                       #Si la probabilidad es mayor al 80%
      name=str(prediction[0][1]*100)+"% Naranja"                     #Indico que es naranja
    else:                                                            #Sino
      name="No es manzana ni naranja"                                #Indico que no es manzana ni naranja
  cv2.putText(imagen, "%s" % (name), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0)) #Escribo en la imagen
  cv2.imshow('Salida', imagen)                                       #Muestro la imagen final

'''/*========================================================================
Funcion: Clasificar
Descripcion: Permite clasificar en tiempo real la fruta que se ve en la camara
Sin parametro de entrada
No retorna nada
========================================================================*/'''
def Clasificar():
  cambiar_texto_label2("Presionar q para salir", "black")                #Cambio texto y color de label2
  while(cap.isOpened()):                                                 #Mientras hay captura
    ret, frame = cap.read()                                              #Tomo frame de la camara
    if ret is True:      
      #Convierto imagen en tensor
      img = cv2.resize(frame, (64, 64), interpolation = cv2.INTER_AREA)
      img_array = image.img_to_array(img) #La convierto a array
      img_batch = np.expand_dims(img_array, axis=0)                      #La convierto a tensor

      #Realizo predicion
      prediction = model.predict(img_batch)                              #Obtengo la prediccion de la imagen
      #print (prediction)                                                 #Imprimo resultado

      if prediction[0][0] > prediction[0][1]:                            #Si la mas probable que sea de la clase 1
        if prediction[0][0] > 0.8:                                       #Si la probabilidad es mayor al 80%
          name=str(prediction[0][0]*100)+"% Manzana"                     #Indico que es una manzana
        else:                                                            #Sino
          name="No es manzana ni naranja"                                #Indico que no es manzana ni naranja
      else:                                                              #Si es mas probable que sea de la clase 2
        if prediction[0][1] > 0.8:                                       #Si la probabilidad es mayor al 80%
          name=str(prediction[0][1]*100)+"% Naranja"                     #Indico que es naranja
        else:                                                            #Sino
          name="No es manzana ni naranja"                                #Indico que no es manzana ni naranja
      cv2.putText(frame, "%s" % (name), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0)) #Escribo la distancia y angulo en el marcador
      cv2.imshow('Salida', frame)                                                 #Muestro el frame final
      if cv2.waitKey(1)&0xFF==ord('q'):                                           #Si se presiona la tecla 'q'
        cv2.destroyWindow('Salida')                                             #Cierro frame camara
        break                                                                   #Salgo del while
  cap.release()                                                   #Limpio la camara

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
entrenar_button = ttk.Button(root, text='Entrenar modelo', command= Entrenar)

#Describo boton para visualizar video por realidad aumentada
guardar_button= ttk.Button(root, text='Guardar modelo', command=Guardar)

#Describo boton para guardar recorte
abrir_button = ttk.Button(root, text='Cargar modelo', command=Abrir)

#Describo boton para guardar recorte
ensayar_button = ttk.Button(root, text='Ensayar modelo', command=Ensayar)

#Describo boton para guardar recorte
clasificar_button = ttk.Button(root, text='Clasificar imagen', command=Clasificar)

#Implemento los botones en el root
entrenar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
guardar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
abrir_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
ensayar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
clasificar_button.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

#Genero un label
label2 = Label(root,text="")
label2.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


#Comienzo la aplicacion
root.mainloop()