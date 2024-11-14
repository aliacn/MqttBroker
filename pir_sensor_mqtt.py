import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from datetime import datetime
import csv

# GPIO ayarlar?
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

# MQTT ayarlar?
MQTT_BROKER = "localhost"
MQTT_TOPIC = "pir/sensor"

# MQTT istemcisi olu?turma
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

def log_data_csv(timestamp, message, pir_value):
    with open("pir_log.csv", "a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([timestamp, message, pir_value])

try:
    print("PIR sensörü izleniyor...")
    while True:
        pir_value = GPIO.input(PIR_PIN)
        if pir_value:
            message = "Hareket algılandı!"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp}: {message} (PIR Degeri: {pir_value})")
            client.publish(MQTT_TOPIC, f"{message} (PIR Degeri: {pir_value})")
            log_data_csv(timestamp, message, pir_value)
            while GPIO.input(PIR_PIN):  # Hareket devam etti?i s�rece bekle
                time.sleep(0.1)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} : Hareket sona erdi.")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program sonlandırılıyor...")
finally:
    GPIO.cleanup()
