# Cloud Asset Management System ☁️

Aplikasi manajemen aset berbasis Cloud yang mengintegrasikan layanan **AWS Serverless** dan **Managed Services**. Sistem ini dirancang untuk menangani siklus hidup data secara otomatis mulai dari pengunggahan, validasi infrastruktur, hingga distribusi aset yang aman.

## 🏗️ Cloud Architecture
Sistem ini dibangun dengan arsitektur **Event-Driven** untuk memastikan skalabilitas dan efisiensi biaya:

* **Compute:** Amazon EC2 (Hosting Flask Web Application)
* **Storage:** Amazon S3 (Object Storage untuk manajemen aset)
* **Database:** Amazon RDS MySQL (Penyimpanan metadata file)
* **Serverless:** AWS Lambda (Otomasi validasi & sanitasi data)

## 🚀 Fitur Utama
- **Automated Production Pipeline:** Memisahkan file mentah di folder `uploads/` dan memindahkannya ke folder `validated/` secara otomatis menggunakan Lambda setelah divalidasi.
- **System Health Monitoring:** Fitur real-time untuk mengecek konektivitas infrastruktur AWS (S3 & RDS) langsung dari dashboard.
- **Secure Asset Delivery:** Menggunakan **S3 Presigned URL** untuk pengunduhan file, memastikan aset tetap private dan hanya bisa diakses melalui token sementara.

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **SDK:** Boto3 (AWS SDK for Python)
- **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome 6
- **Database:** MySQL (Amazon RDS)

## 📁 Struktur Folder S3
- `uploads/`: Landing zone untuk file mentah yang baru diunggah dari Flask.
- `validated/`: Production-ready zone untuk file yang telah divalidasi dan dibersihkan metadatanya oleh Lambda.

## ⚙️ Alur Kerja Data (Workflow)
1. Pengguna mengunggah file gambar melalui dashboard.
2. Flask mengirimkan file ke S3 bucket dalam folder `uploads/`.
3. S3 men-trigger **AWS Lambda** secara otomatis.
4. Lambda memindahkan file ke folder `validated/` dan melakukan *metadata stripping* (opsional).
5. Lambda memanggil endpoint API Flask untuk memperbarui status di **Amazon RDS** menjadi `COMPLETED`.
6. Pengguna melihat status terbaru dan dapat mengunduh file dengan aman melalui Presigned URL.

## 📝 Konfigurasi Environment (.env)
Pastikan file `.env` kamu berisi variabel berikut:
```env
DB_HOST=endpoint-rds-kamu
DB_USER=admin
DB_PASS=password-rds-kamu
DB_NAME=nama_database
BUCKET_NAME=nama-s3-bucket-kamu

Kemudian di dalam lambda function buat env yang berisikan
EC2_IP=ip-ec2-kamu