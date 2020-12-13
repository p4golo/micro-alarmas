from microbit import *

FILAS = 5
PRIMERACOLUMNA = 0
TERCERACOLUMNA = 2
CUARTACOLUMNA = 3
DISPLAYAPAGADO = "00000:00000"
SEGUNDOSALARMA = 0
MAXALARMAS = 5
MILISEGUNDOSASEGUNDOS = 1000
SEGUNDOESPERA = 1
AUMENTOTIEMPO = 1
ESPERAALARMA = 5
CAMBIOTIEMPO = 60
AGITAR = 900

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
    for i in range(FILAS): # Recorre todas las filas y enciende los led de la columna seleccionada con los valores dados
        display.set_pixel(posicion,i,int(numero[0][i]))
    for i in range(FILAS): # Recorre todas las filas y enciende los led de la siguiente columna de la seleccionada con los valores dados
        display.set_pixel(posicion + 1,i,int(numero[1][i]))

def mostrarTiempo(tiempo):
    if tiempo > 9:
        decenas = tiempo // 10
        decenas = fonts[decenas].split(":")
        unidades = tiempo % 10
        unidades = fonts[unidades].split(":")
        mostrarNumeros(decenas,PRIMERACOLUMNA)
        mostrarNumeros(unidades,CUARTACOLUMNA)
    else:
        unidades = fonts[tiempo].split(":")
        mostrarNumeros(unidades,CUARTACOLUMNA)

def limpiarDisplay(): # Pone todos los pixeles del display a 0
    display_apagado = DISPLAYAPAGADO.split(":")
    mostrarNumeros(display_apagado,PRIMERACOLUMNA)
    mostrarNumeros(display_apagado,TERCERACOLUMNA)
    mostrarNumeros(display_apagado,CUARTACOLUMNA)

def establecerTiempoAlarma():
    tiempo_alarma = 0 # Esta funcion establece las horas o minutos de la alarma
    while not button_b.is_pressed(): # Se ejecuta mientras no se pulse b
        mostrarTiempo(tiempo_alarma)
        if button_a.is_pressed(): # Cada vez que se pulse a aumenta el valor de la alarma
            tiempo_alarma += 1
            sleep(500)
        sleep(50)
        limpiarDisplay()
    return tiempo_alarma

def establecerAlarma(lista):
    nueva_lista = [(0,0,0)]*(len(lista)+1) # Creamos una nueva lista de 1 mas de tamaño que la dada
    hora_alarma = establecerTiempoAlarma()
    sleep(500)
    minuto_alarma = establecerTiempoAlarma()
    alarma = (hora_alarma,minuto_alarma,SEGUNDOSALARMA) # Creamos la tupla con la alarma que vamos a introducir
    if len(lista) == 0: # si no hay ninguna alarma, colocamos la actual la primera
        nueva_lista[0] = alarma
    else:
        for i in range(len(lista)): # Recorremos la lista y vamos copiando todos los valores
            nueva_lista[i] = lista[i]
        nueva_lista[len(lista)] = alarma # Añadimos el nuevo valor al final
    return nueva_lista

def alarma():
    for i in range(5): # Durante 5 segundos dibuja una cara alegre y otra triste alternativamente
        display.show(Image.HAPPY)
        sleep(500)
        limpiarDisplay()
        display.show(Image.SAD)
        sleep(500)
        limpiarDisplay()

def ordenarAlarmas(lista):
    if len(lista) > 1: # si el tamaño de la lista es 0 o 1, la lista ya estaria ordenada
        for i in range(len(lista)):
            for j in range(1,len(lista)): # Recorre la lista empezando por el segundo elemento
                if lista[j] < lista[j-1]: # Comprueba si la siguiente alarma es mayor que la actual, si es asi las cambia
                    auxiliar = lista[j]
                    lista[j] = lista[j-1]
                    lista[j-1] = auxiliar

def borrarAlarma(lista):
    lista_nueva = [(0,0,0)]*(len(lista)-1) # Creamos una nueva lista del tamaño de la anterior -1
    for i in range(len(lista)-1): # Recorremos la lista y vamos rellenandola con las alarmas que no han sonado
        lista_nueva[i] = lista[i+1]
    return lista_nueva

def main():
    segundos = 0
    minutos = 0
    horas = 0
    alarmas_pendientes = []
    posx = accelerometer.get_x()
    posy = accelerometer.get_y()

    while True:
        # Si se agita el microbit
        if (posx+AGITAR<accelerometer.get_x() or posx-AGITAR > accelerometer.get_x()) and (posx + AGITAR < accelerometer.get_x() or posx-AGITAR > accelerometer.get_x()):
            if len(alarmas_pendientes) == MAXALARMAS:
                display.scroll("TOO MANY ALARMS")
            else:
                alarmas_pendientes = establecerAlarma(alarmas_pendientes)
                ordenarAlarmas(alarmas_pendientes)
            tiempo = running_time() // MILISEGUNDOSASEGUNDOS # Usamos running_time() para comprobar el tiempo que se ha tardado en poner la alarma
            tiempo = tiempo - (horas*CAMBIOTIEMPO**2+minutos*CAMBIOTIEMPO+segundos)
            if tiempo + segundos >= CAMBIOTIEMPO: # Sumamos el valor obtenido al tiempo actual
                segundos = (tiempo + segundos) - CAMBIOTIEMPO
                minutos += 1
            else:
                segundos += tiempo
        posx = accelerometer.get_x() #Obtenemos nueva posicion x del microbit
        posy = accelerometer.get_y() #Obtenemos nueva posicion y del microbit
        if button_a.is_pressed():
            mostrarTiempo(horas)
            segundos += 1
            sleep(1000)
        if button_b.is_pressed():
            mostrarTiempo(minutos)
            segundos += 1
            sleep(1000)
        tiempo_actual = (horas,minutos,segundos) # Almacenamos en una tupla el tiempo actual para comprobarlo con el de las alarmas
        if len(alarmas_pendientes) > 0:
            if tiempo_actual == alarmas_pendientes[0]: # si el tiempo actual es igual a el valor de la primera alarma, ya que estan ordenadas
                alarma()
                alarmas_pendientes = borrarAlarma(alarmas_pendientes) # Obtenemos la nueva lista sin la alarma que acaba de sonar
                segundos += ESPERAALARMA
        limpiarDisplay()
        mostrarTiempo(segundos)
        sleep(1000) # Para que el bucle tarde un segundo en hacerse
        segundos += 1 # Aumentamos el valor de los segundos
        if segundos == CAMBIOTIEMPO:
            segundos = 0
            minutos += 1
        if minutos == CAMBIOTIEMPO:
            if horas < 99:
                minutos = 0
                horas += 1
            else: # Si llega al maximo del cronometro, se queda en 99 horas 59 minutos y siguen contando los segundos
                horas = 99
                minutos = 59
        limpiarDisplay()

if __name__ == "__main__":
    main()
