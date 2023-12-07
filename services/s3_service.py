import boto3
import json
import os
from config.config_loader import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, AWS_REGION

class S3Service:
    def __init__(self):
        """
        Initializes a new instance of the S3Service class.
        """
        # Read AWS credentials and S3 configuration from config_loader
        self.aws_access_key_id = AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        self.region_name = AWS_REGION  
        self.bucket_name = S3_BUCKET_NAME

        # Create an S3 client
        self.s3_client = boto3.client('s3', aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key,
                                      region_name=self.region_name)

    def send_json_file(self, file_path, object_key):
        """
        Uploads a JSON file to the specified S3 bucket.

        :param file_path: The local path to the JSON file.
        :param object_key: The object key (S3 key) under which the file will be stored.
        :return: True if the upload is successful, False otherwise.
        """
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)

            # Convert JSON data to a string before uploading
            json_string = json.dumps(json_data)

            # Upload the JSON string to S3
            self.s3_client.put_object(Body=json_string, Bucket=self.bucket_name, Key=object_key)

            print(f"JSON file '{file_path}' uploaded to S3 bucket '{self.bucket_name}' with key '{object_key}'.")
            return True

        except Exception as e:
            print(f"Error uploading JSON file to S3: {str(e)}")
            traceback.print_exc()
            return False

# Example Usage:
# Replace 'your_access_key', 'your_secret_key', 'your_region', and 'your_bucket' with your AWS credentials and S3 details.
# s3_service = S3Service(aws_access_key_id='your_access_key', aws_secret_access_key='your_secret_key',
#                        region_name='your_region', bucket_name='your_bucket')
# s3_service.send_json_file(file_path='path/to/your/file.json', object_key='your/object/key.json')
