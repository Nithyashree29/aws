import boto3

def lambda_handler(event, context):
    print("Starting SQL Batch processing")

    queue_url = ''
    sqs = boto3.client("sqs")
    response = sqs.receive_message(
        QueueUrl = queue_url,
        MaxNumberOfMessages = 10,
        WaitTimeSeconds =2
    )

    messages = response.get('Messages', [])
    print("Total messages received in the batch : ", len(messages))
    for message in messages:
        print("Processing message: ", message['body'])
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl = queue_url,
            ReceiptHandle = receipt_handle
        )
        print("Message deleted from the queue")

    print("Ending SQS Batch Process")

    return {
        'StatusCode': 200,
        'body': f'{len(messages)} messages processes and deleted successfully'
    }