import json
import boto3
import random

sqs_client = boto3.client("s3")

QUEUE_URL = ''

def generate_sales_order():
    return {
        "order_id": random.randint(1000, 9999),
        "product_id": random.randint(100, 999),
        "quantity": random.randint(1, 100),
        "price": round(random.uniform(10.0, 500.0), 2)
    }


def lambda_handler(event, context):

    i=0
    while (i<100):
        sales_order = generate_sales_order()
        print(sales_order)
        sqs_client.send_message(
            QueueUrl = QUEUE_URL,
            MessageBody = json.dumps(sales_order)
        )
        i +=1

    return {
        'statusCode': 200,
        'body': json.dumps('Sales order data published to SQS!')
    }