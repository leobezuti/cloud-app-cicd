import boto3
import json
from botocore.exceptions import ClientError

def create_bucket(region='sa-east-1'):
    bucket_name = 'cloud-app-project-1'
    s3 = boto3.client('s3', region_name=region)

    try:
        print(f'Criando o bucket {bucket_name}')
        
        if region != 'us-east-1':
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        else:
            s3.create_bucket(Bucket=bucket_name)

        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )

        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'ErrorDocument': {'Key': 'error.html'},
                'IndexDocument': {'Suffix': 'index.html'},
            }
        )

        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )

        print(f'Bucket configurado com sucesso!')
        print(f'URL: http://{bucket_name}.s3-website-{region}.amazonaws.com')

    except ClientError as e:
        print(f'Erro: {e}')

if __name__ == '__main__':
    create_bucket()