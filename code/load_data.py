import boto3
import csv
import os

# Read AWS credentials from config file
def get_aws_credentials():
    credentials_file = 'configs/rootkey.csv'
    if not os.path.exists(credentials_file):
        raise FileNotFoundError(f"Credentials file not found: {credentials_file}")
    
    with open(credentials_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        credentials = next(reader)
        return credentials['Access key ID'], credentials['Secret access key']

# Get credentials and create S3 client
access_key, secret_key = get_aws_credentials()
s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# Download the restaurant data file from S3
bucket_name = 'restaurant-finder-raw-data'
file_name = 'Restaurants_in_LA_20250907.csv'
local_file_name = 'restaurant-finder-data.csv'

try:
    s3.download_file(bucket_name, file_name, local_file_name)
    print(f"✅ Successfully downloaded '{file_name}' as '{local_file_name}'")
except Exception as e:
    print(f"❌ Error downloading file: {e}")