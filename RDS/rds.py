# # Use this code snippet in your app.
# # If you need more information about configurations
# # or implementing the sample code, visit the AWS docs:
# # https://aws.amazon.com/developer/language/python/

# import boto3
# from botocore.exceptions import ClientError


# def get_secret():

#     secret_name = "dev_mysql_creds"
#     region_name = "ap-southeast-1"

#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )

#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=secret_name
#         )
#     except ClientError as e:
#         # For a list of exceptions thrown, see
#         # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#         raise e

#     secret = get_secret_value_response['SecretString']

#     # Your code goes here.


# Connection String from local mysel server to AWS RDS - mysql -h <host.endpoint> -P 3306 -u admin -p 12341234
# Note - You need to allow inbound traffic in security groups for "MySQL/Aurora" and add any IPV4 allowance.

import base64
import mysql.connector
import boto3
import json

client = boto3.client("secretsmanager", region_name = 'us-east-1')

secret_name = 'mysql-db-creds'

def get_rds_credentials(secret_name):
    try :
        get_secret_value_response = client.get_secret_value(SecretID = secret_name)
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret)
            return secret_dict
        
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            secret_dict = json.loads(decoded_binary_secret)
            return secret_dict

    except Exception as e:
        print(f"Error fetching secret: {e}")
        return None  

def connect_and_create_db():
    try:
        credentials = get_rds_credentials(secret_name)
        if credentials:
            print("RDS Credentials")
            username = credentials['username']
            password = credentials['password']

        else:
            print("Failed to fetch credentials.")

        connection = mysql.connector.conmect(
            host = '',
            port=3306,
            user=username,
            password = password
        )

        if connection.is_connected():
            print("Successfully connected to the RDS instance")
            cursor = connection.cursor()
            cursor.execute("Create DATABASE IF NOT EXISTS TempDB;")
            print("Database created SUCCESSFULLY")

            cursor.execute("SHOW DATABASES;")
            print(cursor.fetchall())

        else:
            print("Failed to connect to the RDS INSTANCE.")
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")

    except Exception as e:
        print("Error : {e}")
    
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    connect_and_create_db()