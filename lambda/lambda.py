import boto3
import urllib.request
import urllib.parse
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']
    
    key = urllib.parse.unquote_plus(raw_key) 
    filename = key.split('/')[-1]
    new_key = f"validated/{filename}"

    try:
        copy_source = f"{bucket}/{key}"
        
        s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=new_key)
        s3.delete_object(Bucket=bucket, Key=key)

        ec2_ip = os.environ.get('EC2_IP')
        url = f"http://{ec2_ip}/update_status/{filename}"
        
        urllib.request.urlopen(url)

        return "File successfully moved to validated folder and Flask notified"
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Failed"
