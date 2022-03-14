import random

def adivinar(intentos=1):
    numero_random = random.randint(0,100)
    for x in range (intentos):
        numero_ingresado=int(input("Ingrese un numero entero: "))
        if (numero_ingresado == numero_random):
            print ("El numero %u fue adivinado en el intento %u".format(numero_random, x))
            break
        else:
            if(numero_ingresado>numero_random):
                print ("El numero a adivinar es menor")
            else:
                print ("El numero a adivinar es mayor")
    else:
        print ("El numero no fue adivinado")

adivinar(5)