from microbit import *

FILAS = 5
PRIMERACOLUMNA = 0
TERCERACOLUMNA = 3

zero = "99999:99999"
one = "00000:99999"
two = "90999:99909"
three = "90909:99999"
four = "99900:09999"
five = "99909:90999"
six = "99999:90999"
seven = "90900:99999"
eight = "99099:99099"
nine = "99900:99999"

fonts = (zero, one, two, three, four, five, six, seven, eight, nine)

def mostrarNumeros(numero,posicion):
    """
        Esta funcion muestra en el panel del microbit un numero dado y en la columna seleccionada.
        @param numero: numero entero de 2 digitos
        @param posicion: numero de la columna en la que se quiere mostrar el numero.
    """
    for i in range(FILAS): # Recorre todas las filas y enciende los led de la columna seleccionada con los valores dados
        display.set_pixel(posicion,i,int(numero[0][i]))
    for i in range(FILAS): # Recorre todas las filas y enciende los led de la siguiente columna de la seleccionada con los valores dados
        display.set_pixel(posicion + 1,i,int(numero[1][i]))

def obtenerDecenas(numero):
    """
        Esta funcion devuelve las decenas del numero dado, con el valor necesario para representarlo en el microbit.
        @param numero: numero entero
    """
    decenas = numero // 10
    decenas = fonts[decenas].split(":")
    return decenas

def obtenerUnidades(numero):
    """
        Esta funcion devuelve las unidades del numero dado, con el valor necesario para representarlo en el microbit.
        @param numero: numero entero
    """
    unidades = numero % 10
    unidades = fonts[unidades].split(":")
    return unidades

def mostrarTiempo(tiempo):
    """
        Esta funcion muestra en el panel del microbit el numero de segundos, minutos o segundos que han pasado.
        @param segundos: numero entero de segundos, minutos o horas que han pasado.
    """
    if tiempo > 9:
        decenas = obtenerDecenas(tiempo)
        unidades = obtenerUnidades(tiempo)
        mostrarNumeros(decenas,PRIMERACOLUMNA)
        mostrarNumeros(unidades,TERCERACOLUMNA)
    else:
        unidades = obtenerUnidades(tiempo)
        mostrarNumeros(unidades,TERCERACOLUMNA)

def establecerTiempoAlarma():
    tiempo_alarma = 0
    while !button_b.is_pressed():
        mostrarTiempo(tiempo_alarma)
        if button_a.is_pressed():
            tiempo_alarma += 1
            sleep(1000)
            segundos += 1
        display.clear()
    return tiempo_alarma

def establecerAlarma():
    hora_alarma = establecerTiempoAlarma()
    minuto_alarma = establecerTiempoAlarma()
    return (hora_alarma,minuto_alarma,0)

def alarma():
    pass

def comprobarNumeroAlarmas():
    if len(lista) > 5:
        display.scrool("TOO MANY ALARMS")

def ordenarAlarmas():
    pass

def main():

    segundos = 0
    minutos = 0
    horas = 0

    while True:
        if button_a.is_pressed():
            mostrarTiempo(horas)
            segundos += 1
            sleep(1000)
        if button_b.is_pressed():
            mostrarTiempo(minutos)
            segundos += 1
            sleep(1000)
        display.clear()
        mostrarTiempo(segundos)
        sleep(1000) # Para que el bucle tarde un segundo en hacerse
        segundos += 1 # Aumentamos el valor de los segundos
        if segundos == 60:
            segundos = 0
            minutos += 1
        if minutos == 60:
            minutos = 0
            horas += 1
        display.clear()

if __name__ == "__main__":
    main()
