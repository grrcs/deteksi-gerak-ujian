import RPi.GPIO as GPIO
import time
import math

# Konfigurasi Pin
BUZZER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Inisialisasi PWM pada pin buzzer
# Parameter awal: Frekuensi 100Hz
pwm = GPIO.PWM(BUZZER_PIN, 100)

def main():
    try:
        pwm.start(50) # Duty Cycle 50% (Volume standar)
        print("Sirine menyala... (Tekan Ctrl+C untuk stop)")
        
        while True:
            # --- FASE NAIK (Suara rendah ke tinggi) ---
            # Range: 500Hz sampai 2000Hz, step 20Hz
            for freq in range(500, 2500, 20):
                pwm.ChangeFrequency(freq)
                time.sleep(0.005) # Delay super kecil agar transisi halus

            # --- FASE TURUN (Suara tinggi ke rendah) ---
            # Range: 2500Hz sampai 500Hz, step -20Hz
            for freq in range(2500, 500, -20):
                pwm.ChangeFrequency(freq)
                time.sleep(0.005)

    except KeyboardInterrupt:
        # Matikan dengan bersih saat di-stop
        print("\nBerhenti.")
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()