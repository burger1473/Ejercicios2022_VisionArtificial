'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 11/04/2022
 * Version: Python 3.7.0
 *          Open CV: 4.5.4-dev
 * Descripcion: Grabo video con framesize automatico
 *===========================================================================*/'''

 #======================== Incluciones ====================================
import cv2

#======================== Variable =======================================
x=0
y=0

#======================== Implementacion==================================

cap = cv2.VideoCapture(1)                                       #Capturo video del dispositivo 0
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')                #Indico codificacion

#Obtengo un frame y miro su tamaño para indicar el framesize del video
if cap.isOpened():                                              #Si hay una captura
    ret2, frame2 = cap.read()                                   #Tomo frame
    x = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))                  #Obtengo tamaño en x
    y = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))                 #Obtengo tamaño en y
    #x=frame2.shape[1]                                          #Obtengo tamaño en x
    #y=frame2.shape[0]                                          #Obtengo tamaño en y


out = cv2.VideoWriter('output.avi', fourcc , 20.0, (x,y))       #Establezo ubicacion, codificacion, framerate y framesize del video a guardar

while(cap.isOpened()):                                          #Mientras hay captura
    ret, frame = cap.read()                                     #Tomo frame
    if ret is True:                                             
        out.write(frame)                                        #Escribo fram en video
        cv2.imshow('frame', frame)                              #Muestro el frame
        if cv2.waitKey(1)&0xFF==ord('q'):                       #Si se presiona la tecla 'q'
            break                                               #Salgo del while
    else:                                                   
        break                                                   #Salgo del while

cap.release()                                                   #Limpio la camara
out.release()                                                   #Limpio el video
cv2.destroyAllWindows()                                         #Cierro todas las ventanas de windows generadas por este codigo
