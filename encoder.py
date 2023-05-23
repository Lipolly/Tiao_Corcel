import RPi.GPIO as GPIO
import time

PIN_A = 17
PIN_B = 18

counter = 0
current_a = 0
current_b = 0

last_count = 0
last_time = time.time()

# Variáveis para cálculo da distância percorrida
pulses_per_rotation = 400 
distance_per_pulse = 0.01
distance = 0

def funcoes(channel):
    global counter, current_a, current_b, last_count, last_time, distance

    current_a = GPIO.input(PIN_A)
    current_b = GPIO.input(PIN_B)

    if current_a != current_b:
        counter += 1
    else:
        counter -= 1

    # Cálculo da velocidade
    current_count = counter
    current_time = time.time()
    delta_count = current_count - last_count
    delta_time = current_time - last_time

    if delta_time > 0:
        velocity = delta_count / delta_time
        print("Velocidade: {:.2f} pulsos/segundo".format(velocity))

    last_count = current_count
    last_time = current_time

    # Cálculo da distância percorrida
    distance += delta_count * distance_per_pulse
    print("Distância percorrida: {:.2f} metros".format(distance))

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(PIN_A, GPIO.BOTH, callback=funcoes)
GPIO.add_event_detect(PIN_B, GPIO.BOTH, callback=funcoes)

try:
    while True:
        rotations = counter / pulses_per_rotation
        print("Rotações: {:.2f}".format(rotations))
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
