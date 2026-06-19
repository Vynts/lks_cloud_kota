## Cloud Asset Manager - LKS Cloud Computing

Aplikasi ini adalah aplikasi berbasis Flask untuk mengelola aset gambar menggunakan layanan-layanan AWS seperti (EC2 sebagai server utama dari aplikasi, 
S3 untuk file system, RDS sebagai database, dan Lambda sebagai function).

cara untuk menjalankan aplikasi, install library yang dibutuhkan dengan command :

buat venv untuk menginstall library untuk python
``` 
sudo apt install python3-venv

sudo python3 -m venv .venv
source .venv/bin/activate
```

install library yang akan digunakan oleh aplikasi
``` 
sudo ./venv/bin/python3 -m pip install -r requirements.txt
```

jalankan aplikasi
``` 
sudo .venv/bin/python3 app.py
```

Ubah file .env yang ada di dalam direktori dengan yang sudah ditentukan
``` 
# Database
DB_HOST = 'yourdatabaseendpoint'
DB_USER = 'yourdatabaseuser'
DB_PASSWORD = 'yourdatabasepassword'
DATABASE = 'yourdatabasename'

# S3 Bucket name
BUCKET_NAME = 'yourbucketname'
```

Setelah itu buat S3 File bucket dan Lambda function, di lambda function tambahkan environment tambahan yaitu EC2_IP = "ip_publik_ec2_kalian", jalankan dengan sesuai dengan contoh yang tertera di soal.


© Dikembangkan oleh Alvinza Erza Farandhika untuk kompetisi LKS Cloud Computing.
