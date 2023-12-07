import boto3
import json
from models.models import UserModel 
from config.config_loader import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, AWS_REGION
from utils.logs_utils import log_error

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

    def s3_init_user(self, user_sub):
        """
        Uploads a JSON representation of the UserModel to the specified S3 bucket.

        :param user_sub: The user_sub variable to include in the UserModel.
        :return: True if the upload is successful, False otherwise.
        """
        try:
            # Create a UserModel instance with the provided user_sub
            user_model = UserModel(user_sub=user_sub)

            # Convert UserModel to a dictionary
            user_data = user_model.model_dump()

            # Convert dictionary to JSON string
            json_string = json.dumps(user_data)

            # Define the object key (S3 key) based on user_sub
            object_key = f"user_data/{user_sub}.json"

            # Upload the JSON string to S3
            self.s3_client.put_object(Body=json_string, Bucket=self.bucket_name, Key=object_key)
            
            log_error(f"User data JSON uploaded to S3 bucket '{self.bucket_name}' with key '{object_key}'.")
            return True

        except Exception as e:
            log_error(f"Error uploading user data JSON to S3: {str(e)}")
            return False

# Example Usage:
# Replace 'your_access_key', 'your_secret_key', 'your_region', and 'your_bucket' with your AWS credentials and S3 details.
# s3_service = S3Service(aws_access_key_id='your_access_key', aws_secret_access_key='your_secret_key',
#                        region_name='your_region', bucket_name='your_bucket')
# s3_service.send_user_model_to_s3(user_sub='example_user_sub')


    def s3_update_user_exercise(self, user_sub, user_exercise_model):
        # TODO: define method
        pass