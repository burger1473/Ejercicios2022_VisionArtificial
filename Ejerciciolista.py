'''/*=============================================================================
 * Author: Fabian Burgos
 * Date: 21/03/2022
 * Version: Python 3.7.0
 *===========================================================================*/'''

#=========================== Variables ================================
tamanio=4  #Tamaño de una matriz cuadrada
Lista_original = [[2,2,5,6], [0,3,7,4], [8,8,5,2], [1,5,6,1]]


#======================== Implementaciones=============================

'''/*========================================================================
Funcion: subarray
Descripcion: Obtiene la sublista o columna indicada
Parametros de entrada:
                      lista: puntero hacia la lista donde se quiere buscar el subarray
                      fila:  numero de la fila que se quiere seleccionar para el subarray
Retorna: Lista del subarray
========================================================================*/'''
def subarray(lista, fila):
    sub=lista[fila]
    return sub

'''/*========================================================================
Funcion: diagonal_cero
Descripcion: coloca ceros en la diagonal de la matriz
Parametros de entrada:
                      lista: puntero hacia la lista donde se quiere aplicar cambios
Retorna: Lista con la diagonal en cero
========================================================================*/'''
def diagonal_cero(lista):    #Escribo la diagonal con ceros
    copia = lista[:] #Copio los valores de lista en la variable diagonal
    
   
    #Forma 1:
    #Solo sirve para matrices cuadrada
    for n in range (tamanio):
        copia[n][n]=0


    #Forma 2:
    '''
    copia[0][0]=0
    copia[1][1]=0
    copia[2][2]=0
    copia[3][3]=0
    '''
    return copia

'''/*========================================================================
Funcion: suma
Descripcion: Suma todos los elementos de la lista
Parametros de entrada:
                      lista: puntero hacia la lista donde se quiere aplicar cambios
Retorna: Valor de la suma
========================================================================*/'''
def suma(lista):  #Suma de elementos
    
    suma=0
    for n in range (tamanio):
        for j in range (tamanio):
            suma=suma+lista[j][n]   
    
    return suma

'''/*========================================================================
Funcion: valor_par_impar
Descripcion: Coloca cero a los elementos pares de la lista y 1 a los elementos impares
Parametros de entrada:
                      lista: puntero hacia la lista donde se quiere aplicar cambios
Retorna: Lista con los valores cambiados
========================================================================*/'''
def valor_par_impar(lista):  #Setear los valores pares en 0 y los impares en 1.
    copia = lista[:]  #Copio los valores de lista en la variable diagonal

    for n in range (tamanio):
        for j in range (tamanio):
            if copia[j][n] % 2 == 0:
                copia[j][n]=0
            else:
                copia[j][n]=1
    
    return copia


'''/*========================================================================
Funcion: main
Descripcion: Funcion principal para seleccionar la accion a realizar
Sin parametros de entrada
No retorna nada
========================================================================*/'''
def main():
    print("Opciones a realizar: \n\n")
    print("1)Seleccionar el subarray \n2)Poner la diagonal de la matriz en cero  \n3)Sumar todos los elementos del array  \n4)Setear los valores pares en 0 y los impares en 1")
    numero_ingresado=int(input("\nIndique la acción a realizar: "))
    print("\nLista original: ")
    print(Lista_original)
    if (numero_ingresado == 1):
        print("\nLista subarray: ")
        print(subarray(Lista_original, 2))
        print("\n\n")
    else:
        if(numero_ingresado == 2):
            print("\nLista con diagonal en cero: ")
            print(diagonal_cero(Lista_original))
            print("\n\n")
        else:
            if(numero_ingresado == 3):
                print("\nValor de la suma: ")
                print(suma(Lista_original))
                print("\n\n")
            else:
                if(numero_ingresado == 4):
                    print("\nValor pares en cero e impares en 1: ")
                    print(valor_par_impar(Lista_original))
                    print("\n\n")
                else:
                    print("\n\nError de seleccion. Reiniciando\n\n")
                    main()

main()
