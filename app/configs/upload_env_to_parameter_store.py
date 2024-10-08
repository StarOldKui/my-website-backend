import os
import boto3
from dotenv import dotenv_values

# Initialize SSM client
ssm = boto3.client("ssm", region_name="us-east-2")  # Replace with your AWS region


def upload_parameter(name, value, type="String"):
    """
    Upload a parameter to AWS Parameter Store
    """
    try:
        ssm.put_parameter(
            Name=name,
            Value=value,
            Type=type,
            Overwrite=True,  # Allow overwriting existing values
        )
        print(f"Uploaded {name} to Parameter Store")
    except Exception as e:
        print(f"Failed to upload {name}: {e}")


def upload_env_to_parameter_store():
    """
    Read the .env file from the actual root directory and upload all variables to Parameter Store
    """
    # Get the absolute path of the project root directory by going 3 levels up
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    env_file_path = os.path.join(project_root, ".env")  # Path to root .env file

    # Load only .env file variables from the root directory
    env_vars = dotenv_values(env_file_path)

    # Iterate through all variables in .env and upload to Parameter Store
    for key, value in env_vars.items():
        if key:  # Ensure that the key is valid and non-empty
            parameter_name = f"/my-website-backend/{key}"
            upload_parameter(parameter_name, value)


if __name__ == "__main__":
    upload_env_to_parameter_store()
