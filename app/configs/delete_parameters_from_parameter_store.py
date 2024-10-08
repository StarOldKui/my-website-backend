import boto3
from botocore.exceptions import ClientError

# Initialize SSM client
ssm = boto3.client("ssm", region_name="us-east-2")  # Replace with your AWS region


def delete_parameters_from_path(path_prefix):
    """
    Delete all parameters under the specified path in AWS Parameter Store
    """
    try:
        # List all parameters under the given path
        response = ssm.get_parameters_by_path(Path=path_prefix, WithDecryption=True)
        parameters = response.get("Parameters", [])

        if not parameters:
            print(f"No parameters found under {path_prefix}.")
            return

        # Delete each parameter by name
        for param in parameters:
            param_name = param["Name"]
            try:
                ssm.delete_parameter(Name=param_name)
                print(f"Deleted {param_name} from Parameter Store")
            except ClientError as e:
                print(f"Failed to delete {param_name}: {e}")
    except ClientError as e:
        print(f"Error retrieving parameters under {path_prefix}: {e}")


if __name__ == "__main__":
    delete_parameters_from_path("/my-website-backend/")
