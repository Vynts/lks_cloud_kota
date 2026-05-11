import boto3
import urllib.request
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    filename = key.split('/')[-1]
    
    new_key = f"validated/{filename}"
    
    try:
        s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': key}, Key=new_key)
        s3.delete_object(Bucket=bucket, Key=key)
        
        ec2_ip = os.environ.get('EC2_IP')
        url = f"http://{ec2_ip}/update_status/{filename}"
        urllib.request.urlopen(url)
        
        return "File moved to resized and Flask notified"
    except Exception as e:
        print(e)
        return "Failed"