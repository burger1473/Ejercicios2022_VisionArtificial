#Declaro variables
tamanio=4  #Tamaño de una matriz cuadrada
Lista_original = [[2,2,5,6], [0,3,7,4], [8,8,5,2], [1,5,6,1]]

def subarray(lista, fila):
    sub=lista[fila]
    return sub

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


def suma(lista):  #Suma de elementos
    
    suma=0
    for n in range (tamanio):
        for j in range (tamanio):
            suma=suma+lista[j][n]   
    
    return suma

def valor_par_impar(lista):  #Setear los valores pares en 0 y los impares en 1.
    copia = lista[:]  #Copio los valores de lista en la variable diagonal

    for n in range (tamanio):
        for j in range (tamanio):
            if copia[j][n] % 2 == 0:
                copia[j][n]=0
            else:
                copia[j][n]=1
    
    return copia

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
