import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from datetime import datetime
import csv
import subprocess

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

# MQTT ayarları
MQTT_BROKER = "localhost"
MQTT_TOPIC = "pir/sensor"

# MQTT istemcisi olusturma
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

def log_data_csv(timestamp, message, pir_value):
    with open("pir_log.csv", "a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([timestamp, message, pir_value])

try:
    print("PIR sensoru izleniyor...")
    while True:
        pir_value = GPIO.input(PIR_PIN)
        if pir_value:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_path = f"/home/pi/myenv/images/{timestamp}.jpg"
            
            # Resim cekme işlemini hemen baslat
            subprocess.run(["libcamera-still", "-o", image_path, "-t", "1"])
            
            message = "Hareket algılandı!"
            print(f"{timestamp}: {message} (PIR Değeri: {pir_value})")
            client.publish(MQTT_TOPIC, f"{message} (PIR Değeri: {pir_value})")
            log_data_csv(timestamp, message, pir_value)
            print(f"Resim cekildi: {image_path}")
            
            while GPIO.input(PIR_PIN):  # Hareket devam ettigi surece bekle
                time.sleep(0.1)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp} : Hareket sona erdi.")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program sonlandırılıyor...")
finally:
    GPIO.cleanup()