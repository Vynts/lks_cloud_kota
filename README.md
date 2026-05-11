## Cloud Asset Manager - LKS Cloud Computing

Aplikasi Flask untuk mengelola aset gambar menggunakan layanan AWS S3, RDS, dan Lambda.

Arsitektur
- EC2: Web Server (Flask)
- S3: Object Storage (Folder uploads dan production)
- RDS: Database MySQL (Metadata file)
- Lambda: Otomasi validasi file dan update status

Fitur Utama
1. Upload dan Monitor: Upload file dan pantau status pemrosesan.
2. System Health: Cek konektivitas S3 dan RDS langsung dari dashboard.
3. Cloud Logs: Melihat riwayat aktivitas file di infrastruktur cloud.
4. Secure Download: Download file menggunakan S3 Presigned URL.
5. Search: Mencari file berdasarkan nama di dalam database.

Alur Kerja
1. User upload file ke S3 folder /uploads.
2. S3 memicu Lambda secara otomatis.
3. Lambda memindahkan file ke folder /production dan update database RDS.
4. Status di dashboard berubah menjadi COMPLETED.

Cara Setup
1. Clone repository ini.
2. Install library: pip install flask boto3 mysql-connector-python python-dotenv
3. Konfigurasi file .env dengan kredensial AWS dan database.
4. Jalankan aplikasi: python app.py

---
Dikembangkan oleh Alvinza Erza Farandhika untuk kompetisi LKS Cloud Computing.