import RPi.GPIO as GPIO
import time

# Liste des GPIO à surveiller (excluant les pins réservés comme 3.3V, 5V, GND)
GPIO_PINS = [2, 3, 4, 17, 27, 22, 10, 9, 11, 0, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21]

def gpio_callback(channel):
    state = GPIO.input(channel)
    print(f"GPIO {channel} has changed to {'HIGH' if state else 'LOW'}")

# Configuration des GPIO
GPIO.setmode(GPIO.BCM)  # Utilisation du mode BCM pour référencer les pins
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=gpio_callback, bouncetime=200)

print("Listening for GPIO changes. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(1)  # Boucle infinie avec pause pour éviter une surcharge CPU
except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()  # Réinitialisation des GPIO avant de quitter
