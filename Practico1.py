'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 14/03/2022
 * Version: Python 3.7.0
 * Descripcion: función adivinar que permita adivinar un número generado en forma aleatoria
 *===========================================================================*/'''

import random

#======================== Implementaciones=============================

'''/*========================================================================
Funcion: adivinar
Descripcion: Funcion que permite adiviar un numero ramdon x intentos
Parametros de entrada:
                      intentos: numero que especifica la cantidad de intentos que se tiene
No retorna nada
========================================================================*/'''
def adivinar(intentos=1):
    numero_random = random.randint(0,100)
    for x in range (intentos):
        numero_ingresado=int(input("Ingrese un numero entero: "))
        if (numero_ingresado == numero_random):
            print ("El numero {} fue adivinado en el intento {}".format(numero_random, x))
            break
        else:
            if(numero_ingresado>numero_random):
                print ("El numero a adivinar es menor")
            else:
                print ("El numero a adivinar es mayor")
    else:
        print ("El numero no fue adivinado")

adivinar(7)