import os
import boto3
from flask import Flask, render_template, request, redirect, jsonify
from dotenv import load_dotenv
from config import db_connection, get_all_files

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

@app.route('/')
def dashboard():
    search_q = request.args.get('q', '')
    data_files = get_all_files(search_q)
    
    return render_template('index.html', files=data_files, search_val=search_q)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        filesize = len(file.read()) // 1024 
        file.seek(0) 

        s3 = boto3.client('s3')
        s3.upload_fileobj(file, os.getenv('BUCKET_NAME'), f"uploads/{filename}")

        conn = db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO gallery (filename, original_size, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (filename, filesize, 'PROCESSING'))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/')

@app.route('/update_status/<filename>')
def update_status(filename):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        query = "UPDATE gallery SET status = 'COMPLETED' WHERE filename = %s"
        cursor.execute(query, (filename,))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print(f"Berhasil update status untuk file: {filename}")
        return "OK", 200 
        
    except Exception as e:
        print(f"Gagal update status: {e}")
        return "Error", 500
    
@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        target_key = f"validated/{filename}"

        s3 = boto3.client('s3')
        s3.delete_object(Bucket=os.getenv('BUCKET_NAME'), Key=target_key)
        
        conn = db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM gallery WHERE filename = %s"
        cursor.execute(query, (filename,))
        conn.commit()
        
        cursor.close()
        conn.close()
        return redirect('/')
        
    except Exception as e:
        print(f"Gagal menghapus: {e}")
        return redirect('/')

@app.route('/download/<filename>')
def download_file(filename):
    try:
        s3 = boto3.client('s3')
        
        bucket_name = os.getenv('BUCKET_NAME')
        
        target_key = f"validated/{filename}"
        
        url = s3.generate_presigned_url('get_object',
            Params={
                'Bucket': bucket_name,
                'Key': target_key,
                'ResponseContentDisposition': f'attachment; filename="hasil_{filename}"'
            },
            ExpiresIn=300 
        )
        return redirect(url)
        
    except Exception as e:
        print(f"Error download: {e}")
        return redirect('/')
    
@app.route('/health-check')
def health_check():
    status = {
        "rds": {"state": "Online", "color": "text-success"},
        "s3": {"state": "Online", "color": "text-success"}
    }
    
    try:
        conn = db_connection()
        conn.ping(reconnect=True) 
        conn.close()
    except Exception:
        status["rds"] = {"state": "Offline", "color": "text-danger"}

    try:
        s3 = boto3.client('s3')
        s3.list_buckets()
    except Exception:
        status["s3"] = {"state": "Offline", "color": "text-danger"}
        
    return jsonify(status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
