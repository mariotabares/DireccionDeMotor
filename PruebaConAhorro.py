import utime
from machine import Pin

# Declaración de puertos
PUL = 7    # Señal pulsada
DIR = 6    # Define la dirección
EN = 5     # Define el enable
DER = 8    # Define la interrupción derecha
IZQ = 9    # Define la interrupción izquierda
PA = 10    # Define la interrupción de pausa

# Configuración de pines
button_pin_derecha = Pin(DER, Pin.IN, Pin.PULL_UP)     # Botón Derecha
button_pin_izquierda = Pin(IZQ, Pin.IN, Pin.PULL_UP)   # Botón Izquierda
button_pin_pausa = Pin(PA, Pin.IN, Pin.PULL_UP)        # Botón Pausa
pul_pin = Pin(PUL, Pin.OUT)
dir_pin = Pin(DIR, Pin.OUT)
en_pin = Pin(EN, Pin.OUT)

# Estado inicial y variables de control
paused = True  # Inicia en pausa para modo ahorro de energía
current_direction = None  # Variable para almacenar la dirección actual del movimiento

# Variables para debounce
debounce_delay = 500  # Retardo de debounce en milisegundos
last_interrupt_time = 0  # Variable para almacenar el tiempo de la última interrupción

# Funciones de manejo de interrupción con debounce
def button_interrupt_handler_derecha(pin):
    global paused, current_direction, last_interrupt_time
    current_time = utime.ticks_ms()
    if current_time - last_interrupt_time > debounce_delay:
        last_interrupt_time = current_time
        if not paused:
            current_direction = "derecha"
            dir_pin.value(0)   # Dirección hacia la derecha
            en_pin.value(1)
            print("Iniciando movimiento a la derecha")

def button_interrupt_handler_izquierda(pin):
    global paused, current_direction, last_interrupt_time
    current_time = utime.ticks_ms()
    if current_time - last_interrupt_time > debounce_delay:
        last_interrupt_time = current_time
        if not paused:
            current_direction = "izquierda"
            dir_pin.value(1)   # Dirección hacia la izquierda
            en_pin.value(1)
            print("Iniciando movimiento a la izquierda")

def button_interrupt_handler_pausa(pin):
    global paused, last_interrupt_time
    current_time = utime.ticks_ms()
    if current_time - last_interrupt_time > debounce_delay:
        last_interrupt_time = current_time
        if paused:
            print("Continuar")
            paused = False
            en_pin.value(1)  # Habilitar el motor
        else:
            print("Pausa")
            paused = True
            en_pin.value(0)  # Deshabilitar el motor

# Configuración de interrupciones
button_pin_derecha.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt_handler_derecha)
button_pin_izquierda.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt_handler_izquierda)
button_pin_pausa.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt_handler_pausa)

# Bucle principal
while True:
    if not paused:
        if current_direction == "derecha":
            dir_pin.value(0)   # Dirección hacia la derecha
            en_pin.value(1)
            while not paused:  # Continuar girando mientras no esté pausado
                pul_pin.value(1)
                utime.sleep_us(400)
                pul_pin.value(0)
                utime.sleep_us(400)

        elif current_direction == "izquierda":
            dir_pin.value(1)   # Dirección hacia la izquierda
            en_pin.value(1)
            while not paused:  # Continuar girando mientras no esté pausado
                pul_pin.value(1)
                utime.sleep_us(400)
                pul_pin.value(0)
                utime.sleep_us(400)

    else:
        en_pin.value(0)  # Deshabilitar el motor cuando está en pausa
        utime.sleep_ms(100)  # Pequeña pausa para reducir el uso de CPU
