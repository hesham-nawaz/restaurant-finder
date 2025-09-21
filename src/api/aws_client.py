"""
AWS S3 client for data operations.
"""

import boto3
import csv
import os
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, List, Dict, Any


class AWSClient:
    """Client for AWS S3 operations."""
    
    def __init__(self, credentials_file: str = 'configs/rootkey.csv'):
        """
        Initialize the AWS client.
        
        Args:
            credentials_file: Path to AWS credentials CSV file
        """
        self.credentials_file = credentials_file
        self.s3_client = self._create_s3_client()
    
    def _get_aws_credentials(self) -> tuple[str, str]:
        """Read AWS credentials from config file."""
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")
        
        with open(self.credentials_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            credentials = next(reader)
            return credentials['Access key ID'], credentials['Secret access key']
    
    def _create_s3_client(self) -> boto3.client:
        """Create and return S3 client."""
        try:
            access_key, secret_key = self._get_aws_credentials()
            return boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
        except Exception as e:
            raise Exception(f"Failed to create S3 client: {e}")
    
    def test_connection(self) -> bool:
        """Test S3 connection and list available buckets."""
        try:
            response = self.s3_client.list_buckets()
            print("✅ Successfully connected to AWS S3")
            print("Available buckets:")
            for bucket in response['Buckets']:
                print(f"  - {bucket['Name']} (created: {bucket['CreationDate']})")
            return True
        except NoCredentialsError:
            print("❌ AWS credentials not found or invalid")
            return False
        except ClientError as e:
            print(f"❌ AWS connection error: {e}")
            return False
    
    def check_bucket_access(self, bucket_name: str) -> bool:
        """Check if we can access the specific bucket."""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' is accessible")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"❌ Bucket '{bucket_name}' does not exist")
            elif error_code == '403':
                print(f"❌ Access denied to bucket '{bucket_name}' - check permissions")
            else:
                print(f"❌ Error accessing bucket '{bucket_name}': {e}")
            return False
    
    def list_bucket_contents(self, bucket_name: str) -> List[Dict[str, Any]]:
        """List contents of the bucket."""
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                print(f"Files in bucket '{bucket_name}':")
                for obj in response['Contents']:
                    print(f"  - {obj['Key']} ({obj['Size']} bytes, modified: {obj['LastModified']})")
                return response['Contents']
            else:
                print(f"Bucket '{bucket_name}' is empty")
                return []
        except ClientError as e:
            print(f"❌ Error listing bucket contents: {e}")
            return []
    
    def download_file(self, bucket_name: str, file_name: str, local_file_name: str) -> bool:
        """
        Download a file from S3.
        
        Args:
            bucket_name: Name of the S3 bucket
            file_name: Name of the file in S3
            local_file_name: Local path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(local_file_name), exist_ok=True)
            
            self.s3_client.download_file(bucket_name, file_name, local_file_name)
            print(f"✅ Successfully downloaded '{file_name}' as '{local_file_name}'")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                print(f"❌ File '{file_name}' not found in bucket '{bucket_name}'")
            elif error_code == '403':
                print(f"❌ Access denied to file '{file_name}' - check permissions")
            else:
                print(f"❌ Error downloading file: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def upload_file(self, local_file_name: str, bucket_name: str, file_name: str) -> bool:
        """
        Upload a file to S3.
        
        Args:
            local_file_name: Local path to the file
            bucket_name: Name of the S3 bucket
            file_name: Name for the file in S3
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.s3_client.upload_file(local_file_name, bucket_name, file_name)
            print(f"✅ Successfully uploaded '{local_file_name}' to '{bucket_name}/{file_name}'")
            return True
        except ClientError as e:
            print(f"❌ Error uploading file: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
