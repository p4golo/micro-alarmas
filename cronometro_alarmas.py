from microbit import *

FILAS = 5
PRIMERACOLUMNA = 0
TERCERACOLUMNA = 3
DISPLAYAPAGADO = "00000:00000"
SEGUNDOSALARMA = 0
MAXALARMAS = 5

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

def mostrarTiempo(tiempo):
    """
        Esta funcion muestra en el panel del microbit el numero de segundos, minutos o segundos que han pasado.
        @param segundos: numero entero de segundos, minutos o horas que han pasado.
    """
    if tiempo > 9:
        decenas = tiempo // 10
        decenas = fonts[decenas].split(":")
        unidades = tiempo % 10
        unidades = fonts[unidades].split(":")
        mostrarNumeros(decenas,PRIMERACOLUMNA)
        mostrarNumeros(unidades,TERCERACOLUMNA)
    else:
        unidades = fonts[tiempo].split(":")
        mostrarNumeros(unidades,TERCERACOLUMNA)

def limpiarDisplay():
    """
        Esta funcion apaga todos los pixeles del display,seria un equivalente a display.clear().
    """
    display_apagado = DISPLAYAPAGADO.split(":")
    mostrarNumeros(display_apagado,PRIMERACOLUMNA)
    mostrarNumeros(display_apagado,TERCERACOLUMNA)

def establecerTiempoAlarma():
    tiempo_alarma = 0
    while not button_b.is_pressed():
        mostrarTiempo(tiempo_alarma)
        if button_a.is_pressed():
            tiempo_alarma += 1
            sleep(500)
        display.clear()
    return tiempo_alarma

def establecerAlarma(lista):
    nueva_lista = [(0,0,0)]*(len(lista)+1)
    hora_alarma = establecerTiempoAlarma()
    sleep(1000)
    minuto_alarma = establecerTiempoAlarma()
    alarma = (hora_alarma,minuto_alarma,SEGUNDOSALARMA)
    if len(lista) == 0:
        nueva_lista[0] = alarma
    else:
        for i in range(len(lista)):
            nueva_lista[i] = lista[i]
        nueva_lista[len(lista)] = alarma
    return nueva_lista

def alarma():
    for i in range(5):
        display.show(Image.HAPPY)
        sleep(500)
        display.clear()
        display.show(Image.SAD)
        sleep(500)
        display.clear()

def ordenarAlarmas(lista):
    if len(lista) > 1:
        for i in range(len(lista)):
            for j in range(1,len(lista)):
                if lista[j] < lista[j-1]:
                    auxiliar = lista[j]
                    lista[j] = lista[j-1]
                    lista[j-1] = auxiliar

def borrarAlarma(lista):
    lista_nueva = [(0,0,0)]*(len(lista))
    for i in range(len(lista)-1):
        lista_nueva[i] = lista[i+1]
    return lista_nueva

def main():

    segundos = 0
    minutos = 0
    horas = 0
    alarmas_pendientes = []

    while True:
        if accelerometer.was_gesture("shake"):
            if len(alarmas_pendientes) == MAXALARMAS:
                display.scroll("TOO MANY ALARMS")
            else:
                alarmas_pendientes = establecerAlarma(alarmas_pendientes)
                ordenarAlarmas(alarmas_pendientes)
        if button_a.is_pressed():
            mostrarTiempo(horas)
            segundos += 1
            sleep(1000)
        if button_b.is_pressed():
            mostrarTiempo(minutos)
            segundos += 1
            sleep(1000)
        tiempo_actual = (horas,minutos,segundos)
        if len(alarmas_pendientes) > 0:
            if tiempo_actual == alarmas_pendientes[0]:
                alarma()
                alarmas_pendientes = borrarAlarma(alarmas_pendientes)
                segundos += 5
        limpiarDisplay()
        mostrarTiempo(segundos)
        sleep(1000) # Para que el bucle tarde un segundo en hacerse
        segundos += 1 # Aumentamos el valor de los segundos
        if segundos == 60:
            segundos = 0
            minutos += 1
        if minutos == 60:
            minutos = 0
            horas += 1
        limpiarDisplay()

if __name__ == "__main__":
    main()

