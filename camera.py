import subprocess

def start_camera_preview():
    try:
        print("Kamera önizleme baslatiliyor...")
        # Kamera önizleme penceresini başlat ve kullan?c? kapatana kadar a�?k tut
        subprocess.run(["libcamera-hello", "--qt-preview", "-t", "0", "--width", "4056", "--height", "3040"])
    except KeyboardInterrupt:
        print("�nizleme sonlanırılıyor...")

if __name__ == "__main__":
    start_camera_preview()