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

def mostrarSegundos(segundos):
    """
        Esta funcion muestra en el panel del microbit el numero de segundos que han pasado.
        @param segundos: numero entero de segundos que han pasado.
    """
    if segundos > 9:
        decenas = obtenerDecenas(segundos)
        unidades = obtenerUnidades(segundos)
        mostrarNumeros(decenas,PRIMERACOLUMNA)
        mostrarNumeros(unidades,TERCERACOLUMNA)
    else:
        unidades = obtenerUnidades(segundos)
        mostrarNumeros(unidades,TERCERACOLUMNA)

def mostrarHoras(horas):
    """
        Esta funcion muestra en el panel del microbit el numero de horas que han pasado.
        @param horas: numero entero de horas que han pasado.
    """
    if horas > 9:
        decenas = obtenerDecenas(horas)
        unidades = obtenerUnidades(horas)
        mostrarNumeros(decenas,PRIMERACOLUMNA)
        mostrarNumeros(unidades,TERCERACOLUMNA)
    else:
        unidades = obtenerUnidades(horas)
        mostrarNumeros(unidades,TERCERACOLUMNA)
    sleep(1000)

def mostrarMinutos(minutos):
    """
        Esta funcion muestra en el panel del microbit el numero de minutos que han pasado.
        @param minutos: numero entero de minutos que han pasado.
    """
    if minutos > 9:
        decenas = obtenerDecenas(minutos)
        unidades = obtenerUnidades(minutos)
        mostrarNumeros(decenas,PRIMERACOLUMNA)
        mostrarNumeros(unidades,TERCERACOLUMNA)
    else:
        unidades = obtenerUnidades(minutos)
        mostrarNumeros(unidades,TERCERACOLUMNA)
    sleep(1000)

def main():

    segundos = 0
    minutos = 0
    horas = 0

    while True:
        if button_a.is_pressed():
            mostrarHoras(horas)
            segundos += 1
            display.clear()
        if button_b.is_pressed():
            mostrarMinutos(minutos)
            segundos += 1
            display.clear()
        mostrarSegundos(segundos)
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
