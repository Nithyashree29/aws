import mysql.connector
import boto3
import json

# Initialize a Secrets Manager client
client = boto3.client('secretsmanager', region_name='us-east-1')

secret_name = 'mysql-db-creds'

def get_rds_credentials(secret_name):
    try:
        # Fetch the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        # Check if the secret uses the Secrets Manager binary field
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
    connection = None

    try:

        credentials = get_rds_credentials(secret_name)
        if credentials:
            print("Fecthed RDS Credentials:")
            username = credentials['username']
            password = credentials['password']
            # Depending on how you've structured your secret, you might need
            # to adjust the keys (e.g., 'username' and 'password') accordingly.
        else:
            print("Failed to fetch credentials.")

        connection = mysql.connector.connect(
            host='rds-mysql-dev.c5gs6yamcv34.us-east-1.rds.amazonaws.com',
            port=3306,
            user=username,
            password=password
        )

        if connection.is_connected():
            print("Successfully connected to the RDS instance.")
            
            cursor = connection.cursor()
            
            # Create a new database
            cursor.execute("CREATE DATABASE IF NOT EXISTS DemoDB;")
            print("Database created successfully.")
            
            cursor.execute("SHOW DATABASES;")
            print(cursor.fetchall())
            
        else:
            print("Failed to connect to the RDS instance.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    connect_and_create_db()