import boto3
import json
from models.models import UserModel, TrainerModel , UserExerciseModel, RecordsModel
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
        
    

    def s3_init_user_records(self, user_sub):
        """
        Initializes user records in an S3 bucket by creating a RecordsModel instance and uploading its data as JSON.

        Parameters:
            - user_sub (str): The sub (subject) identifier of the user.

        Returns:
            - bool: True if the upload is successful, False otherwise.

        Example:
            ```python
            cognito_service = CognitoService()
            user_sub_value = "user123"
            success = cognito_service.s3_init_user_records(user_sub=user_sub_value)
            print(success)
            ```

        Note:
            - The RecordsModel class must have a method `model_dump` that returns the model data as a dictionary.
            - Make sure to handle exceptions appropriately when calling this method.
            - The uploaded data is stored in an S3 bucket with a key based on the user_sub.
        """
        try:
            # Create a UserModel instance with the provided user_sub
            records_model = RecordsModel(user_sub=user_sub)

            # Convert UserModel to a dictionary
            user_data = records_model.model_dump()

            # Convert dictionary to JSON string
            json_string = json.dumps(user_data)

            # Define the object key (S3 key) based on user_sub
            object_key = f"user_records/{user_sub}.json"

            # Upload the JSON string to S3
            self.s3_client.put_object(Body=json_string, Bucket=self.bucket_name, Key=object_key)
            
            log_error(f"User data JSON uploaded to S3 bucket '{self.bucket_name}' with key '{object_key}'.")
            return True

        except Exception as e:
            log_error(f"Error uploading user data JSON to S3: {str(e)}")
            return False



    def s3_update_user_exercise(self, user_sub, user_exercise_model: UserExerciseModel):
        """
        Uploads a JSON representation of the UserExerciseModel to the specified S3 bucket.

        :param user_sub: The user_sub variable to include in the UserExerciseModel.
        :param user_exercise_model: The UserExerciseModel instance to upload.
        :return: True if the upload is successful, False otherwise.
        """
        try:
            # Convert UserExerciseModel to a dictionary
            user_data = user_exercise_model.model_dump()

            # Convert dictionary to JSON string
            json_string = json.dumps(user_data)

            # Define the object key (S3 key) based on user_sub
            object_key = f"user_data/{user_sub}.json"

            # Upload the JSON string to S3
            self.s3_client.put_object(Body=json_string, Bucket=self.bucket_name, Key=object_key)

            log_error(f"User exercise data JSON uploaded to S3 bucket '{self.bucket_name}' with key '{object_key}'.")
            return True

        except Exception as e:
            log_error(f"Error uploading user exercise data JSON to S3: {str(e)}")
            return False
        


    def s3_get_user_data(self, user_sub):
        """
        Retrieves the user_data JSON file from the specified S3 bucket.
        

        :param user_sub: The user_sub variable to include in the UserModel.
        :return: The user_data as a dictionary if the download is successful, None otherwise.
        """
        try:
            # Define the object key (S3 key) based on user_sub
            object_key = f"user_data/{user_sub}.json"

            # Download the JSON file from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)

            # Parse the JSON string
            user_data_json = response['Body'].read().decode('utf-8')
            user_data = json.loads(user_data_json)
            
            return user_data

        except Exception as e:
            log_error(f"Error retrieving user data JSON from S3: {str(e)}")
            return None
        


    def get_student_list(self, trainer_sub):
        """
        Retrieves the list of students for the specified trainer from the S3 bucket.

        :param trainer_sub: The trainer_sub variable to include in the object key.
        :return: The list of students as a list of dictionaries if the download is successful, None otherwise.
        """
        try:
            # Define the object key (S3 key) for the trainer's JSON file based on trainer_sub
            object_key = f"trainer_data/{trainer_sub}.json"

            # Download the JSON file from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)

            # Parse the JSON string
            trainer_data_json = response['Body'].read().decode('utf-8')
            trainer_data = json.loads(trainer_data_json)

            # Retrieve and return the student list from the trainer's data
            student_list = trainer_data.get('students', [])
            return student_list

        except Exception as e:
            log_error(f"Error retrieving student list JSON from S3: {str(e)}")
            return None
        


    def add_student_to_list(self, trainer_model: TrainerModel):
        """
        Adds a TrainerModel instance to a list by converting it to JSON and uploading it to an S3 bucket.

        Parameters:
            - trainer_model (TrainerModel): The TrainerModel instance to be added to the list.

        Returns:
            - bool: True if the upload is successful, False otherwise.

        Example:
            ```python
            cognito_service = CognitoService()
            trainer_instance = TrainerModel(...)  # Create a TrainerModel instance
            success = cognito_service.add_student_to_list(trainer_instance)
            print(success)
            ```

        Note:
            - The TrainerModel class must have a method `model_dump` that returns the model data as a dictionary.
            - Make sure to handle exceptions appropriately when calling this method.
        """
        try:
            # Convert TrainerModel to a dictionary
            trainer_data = trainer_model.model_dump()  

            # Convert dictionary to JSON string
            json_string = json.dumps(trainer_data)

            # Define the object key (S3 key) based on the model name
            object_key = f"trainer_data/{trainer_model.user_sub}.json"

            # Upload the JSON string to S3
            self.s3_client.put_object(Body=json_string, Bucket=self.bucket_name, Key=object_key)

            print(f"Trainer data JSON uploaded to S3 bucket '{self.bucket_name}' with key '{object_key}'.")
            return True

        except Exception as e:
            print(f"Error uploading trainer data JSON to S3: {str(e)}")
            return False
        

    def get_user_records(self, user_sub):
        """
        Retrieves the fitness records for the specified user from the S3 bucket.

        :param user_sub: The user_sub variable to include in the object key.
        :return: The list of fitness records as a list of dictionaries if the download is successful, None otherwise.
        """
        try:
            # Define the object key (S3 key) for the user's JSON file based on user_sub
            object_key = f"user_records/{user_sub}.json"

            # Download the JSON file from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)

            # Parse the JSON string
            user_data_json = response['Body'].read().decode('utf-8')
            user_data = json.loads(user_data_json)

            # Retrieve and return the fitness records list from the user's data
            records_list = user_data.get('records_list', [])
            return records_list

        except Exception as e:
            log_error(f"Error retrieving fitness records JSON from S3: {str(e)}")
            return None
        

    def update_user_records(self, records_model: RecordsModel):
        """
        Updates the fitness records for the specified user in the S3 bucket.

        :param user_model: An instance of the RecordsModel containing the updated fitness records.
        :return: True if the update is successful, False otherwise.
        """
        try:
            # Convert RecordsModel to a dictionary
            user_data = records_model.model_dump()

            # Convert dictionary to JSON string
            json_string = json.dumps(user_data)

            # Define the object key (S3 key) based on the user's identifier
            object_key = f"user_records/{records_model.user_sub}.json"

            # Upload the JSON string to S3
            self.s3_client.put_object(Body=json_string, Bucket=self.bucket_name, Key=object_key)

            log_error(f"User data JSON updated on S3 bucket '{self.bucket_name}' with key '{object_key}'.")
            return True

        except Exception as e:
            log_error(f"Error updating user data JSON on S3: {str(e)}")
            return False