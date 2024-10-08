import os
import boto3
from botocore.exceptions import ClientError
from app.utils.logger_util import LoggerUtil

# Initialize the logger
logger = LoggerUtil.get_logger()


class Config:
    def __init__(self, path_prefix):
        self.ssm = boto3.client("ssm", region_name="us-east-2")
        self.path_prefix = path_prefix

    def load_parameters(self):
        """
        Load all parameters from the specified path in AWS Parameter Store
        and set them as environment variables.
        """
        try:
            # Log the attempt to fetch parameters
            logger.info(f"Fetching parameters from {self.path_prefix}")

            # Fetch parameters from the path prefix
            response = self.ssm.get_parameters_by_path(
                Path=self.path_prefix, WithDecryption=True
            )
            parameters = response.get("Parameters", [])

            if not parameters:
                logger.warning(f"No parameters found under {self.path_prefix}")
            else:
                logger.info(
                    f"Found {len(parameters)} parameters under {self.path_prefix}"
                )

            for param in parameters:
                # Extract parameter name and value
                param_name = param["Name"].replace(self.path_prefix, "").lstrip("/")
                param_value = param["Value"]

                # Set the parameter as an environment variable
                os.environ[param_name] = param_value
                logger.info(f"Loaded parameter {param_name} into environment")

        except ClientError as e:
            logger.error(f"Error retrieving parameters under {self.path_prefix}: {e}")
            logger.debug(e, exc_info=True)


# Function to load parameters from the /my-website-backend/ path
def load_env_from_parameter_store():
    config = Config("/my-website-backend/")  # Path to the parameters in Parameter Store
    config.load_parameters()


if __name__ == "__main__":
    load_env_from_parameter_store()
