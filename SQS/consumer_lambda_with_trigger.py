import json
def process_sales_order(sales_order):
    print(sales_order)

def lambda_handler(event, context):
    print("Starting SQS Batch Process")
    print("Messages received in current batch = ", len(event['Records']))

    for record in event['Records']:
        sales_order = json.loads(record['body'])
        process_sales_order(sales_order)

    print("Ending SQS Batch Process")
    return {
        'statusCode': 200,
        'body': json.dumps('processed sales orders from SQS!')
    }