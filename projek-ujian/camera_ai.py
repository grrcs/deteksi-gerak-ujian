import cv2
import mediapipe as mp
import numpy as np
import mysql.connector 
from datetime import datetime
import time

# Cek library GPIO (Biar aman kalau dites di laptop)
try:
    from gpiozero import Buzzer
    IS_RASPBERRY_PI = True
except ImportError:
    IS_RASPBERRY_PI = False

class ProctorAI:
    def __init__(self):
        # --- KONFIGURASI DATABASE ---
        # Pastikan Laptop & Raspberry Pi konek di Wi-Fi yang sama (Hotspot HP)
        self.db_config = {
            'host': '172.20.10.4',   # <--- IP Laptop kamu (dari ipconfig tadi)
            'user': 'admin',         # User yang baru dibuat ulang
            'password': '123',       # Password user admin
            'database': 'proctor_db' # Nama database di HeidiSQL
        }

        # Koneksi awal ke Database
        self.connect_db()
        self.last_log_time = 0 

        # --- SETUP AI (OPTIMASI SPEED) ---
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False, # False biar ringan di Raspberry Pi
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.status = "AMAN"
        self.cap = cv2.VideoCapture(0)
        
        # Turunkan resolusi biar FPS tinggi
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Setting Skip Frame (Biar tidak lag)
        self.frame_count = 0
        self.skip_rate = 2 

        # Setup Buzzer di GPIO 17
        if IS_RASPBERRY_PI:
            self.buzzer = Buzzer(17)
        else:
            self.buzzer = None

    def connect_db(self):
        """Fungsi untuk menyambung ulang jika putus"""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            print(">> BERHASIL KONEK KE DATABASE LAPTOP!")
        except mysql.connector.Error as err:
            print(f">> GAGAL KONEK DATABASE: {err}")
            self.conn = None

    def log_to_db(self, status_pelanggaran):
        current_time = time.time()
        
        # Cooldown 2 detik (jangan nyepam database)
        if current_time - self.last_log_time > 2.0:
            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Cek koneksi, kalau putus coba sambung lagi
            if self.conn is None or not self.conn.is_connected():
                print("Koneksi putus, mencoba reconnect...")
                self.connect_db()

            if self.conn and self.conn.is_connected():
                try:
                    # Query Insert MySQL
                    sql = "INSERT INTO logs_ujian (waktu, status_siswa, keterangan) VALUES (%s, %s, %s)"
                    val = (waktu_sekarang, status_pelanggaran, "Terdeteksi Curang")
                    
                    self.cursor.execute(sql, val)
                    self.conn.commit()
                    
                    print(f"[LOG] Tersimpan: {status_pelanggaran} -> {waktu_sekarang}")
                    self.last_log_time = current_time
                except mysql.connector.Error as err:
                    print(f"Gagal simpan data: {err}")

    def get_frame(self):
        success, image = self.cap.read()
        if not success:
            return None, "Kamera Error"

        image = cv2.resize(image, (640, 480))
        image = cv2.flip(image, 1) 
        
        self.frame_count += 1
        
        # --- PROSES AI (Hanya jalan 1x setiap 3 frame) ---
        if self.frame_count % (self.skip_rate + 1) == 0:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(image_rgb)
            
            should_buzz = False 
            self.status = "FOKUS" 

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    nose_tip = face_landmarks.landmark[1]
                    left_edge = face_landmarks.landmark[234]
                    right_edge = face_landmarks.landmark[454]

                    dist_to_left = abs(nose_tip.x - left_edge.x)
                    dist_to_right = abs(nose_tip.x - right_edge.x)
                    total_width = dist_to_left + dist_to_right
                    
                    if total_width != 0: ratio = dist_to_left / total_width
                    else: ratio = 0.5

                    # Logika Tengok
                    if ratio < 0.20:
                        self.status = "TENGOK KIRI"
                        should_buzz = True
                    elif ratio > 0.80:
                        self.status = "TENGOK KANAN"
                        should_buzz = True
                    
                    # Logika Nunduk
                    if nose_tip.y > 0.75: 
                        self.status = "MENUNDUK"
                        should_buzz = True
            else:
                self.status = "WAJAH HILANG"
                should_buzz = True

            # --- LOGIKA KONTROL BUZZER & DB ---
            if should_buzz:
                if self.buzzer and not self.buzzer.is_active: self.buzzer.on()
                # Simpan pelanggaran ke database
                self.log_to_db(self.status) 
            else:
                if self.buzzer and self.buzzer.is_active: self.buzzer.off()
        
        # --- VISUALISASI ---
        if self.status == "FOKUS": text_color = (0, 255, 0)
        else: text_color = (0, 0, 255)

        cv2.putText(image, f"STATUS: {self.status}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)
        cv2.putText(image, f"STATUS: {self.status}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70] 
        ret, jpeg = cv2.imencode('.jpg', image, encode_param)
        return jpeg.tobytes(), self.status

    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None and self.conn.is_connected():
            self.conn.close()
        if self.buzzer:
            self.buzzer.off()
            self.buzzer.close()
        self.cap.release()