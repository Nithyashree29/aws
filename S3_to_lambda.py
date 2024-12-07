import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # Get the s3 bucket and object key from the lambda event trigger
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # use boto3 to get the csv file from s3
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket = bucket, Key = key)
    file_content = response['Body'].read().decods('utf-8')

    # Read the content using pandas
    data = pd.read_csv(StringIO(file_content))
    print("the data is", data)