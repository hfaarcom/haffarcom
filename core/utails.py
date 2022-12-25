import botocore
import boto3
from django.conf import settings


secret_key = settings.DJ_SECRET_KEY
public_key = settings.DJ_PUBLIC_KEY

bucket = settings.DJ_BUCKET_NAME

session = boto3.session.Session()

client = session.client('s3',
                        config=botocore.config.Config(
                            s3={'addressing_style': 'virtual'}),
                        endpoint_url='https://fra1.digitaloceanspaces.com',
                        aws_secret_access_key=secret_key,
                        aws_access_key_id=public_key,
                        )


def uploadfile(file, name, type):

    client.put_object(Bucket=bucket,
                      Key=name,
                      Body=file,
                      ACL='public-read',
                      ContentType=f'image/{type}'
                      )
    url = f'https://haffar.fra1.cdn.digitaloceanspaces.com/{name}'
    return url


# check if file name exists in space

def checkFile(name):
    response = client.list_objects(Bucket=bucket)
    for obj in response['Contents']:
        if name == obj['Key']:
            return False
    return True
