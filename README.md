# My Website Backend: Python Docker on AWS Lambda

This project demonstrates running a Python Docker image on AWS Lambda, leveraging AWS Parameter Store to securely manage
environment variables.

# Setup Instructions

## 1. Create a .env File Locally

Before deploying or running the application, create a .env file in the root of the project.
This file will hold
sensitive configuration details such as API keys and endpoint URLs.

```
# OpenAPI
OPENAI_API_KEY=...

# LangSmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=my-website-backend
```

## 2. Upload Environment Variables to AWS Parameter Store

Since the .env file is for local use only, you need to upload these environment variables to AWS Parameter Store so they
can be accessed by the Lambda function running the Docker image.

You can use the provided upload_env_to_parameter_store.py script to upload all the variables in your .env file to AWS
Parameter Store:

```shell
python app/configs/upload_env_to_parameter_store.py
```

This script will read the .env file and upload each key-value pair to AWS Systems Manager (SSM) Parameter Store, under
the /my-website-backend/ path.

# 3. Build and Test Docker Image Locally

You can build and run the Docker image locally to test it before deploying to AWS Lambda. Ensure you are building the
image for a Linux platform, as required by AWS Lambda.

```shell
docker build --platform linux/amd64 -t my-website-backend-image:test .
```

```shell
docker run --platform linux/amd64 -p 9000:8080 --read-only my-website-backend-image:test
```

This command will:

- Run the Docker container on port 9000.
- Use the --read-only flag for security purposes, ensuring that the filesystem remains read-only inside the container.

## 4. Deploy to AWS Lambda, Docker, and CI/CD Pipeline Using AWS CDK

This project uses the **AWS Cloud Development Kit (CDK) with Python** to deploy the following components:
- **Lambda function**: Runs a Docker image to process requests.
- **Docker image**: Built and deployed to AWS Elastic Container Registry (ECR).
- **CI/CD Pipeline (CodePipeline)**: Automatically builds, tests, and deploys the Lambda function whenever new code is committed to the repository.

#### Initial CDK Deployment

Before automating the deployment process with the CI/CD pipeline, you need to run the initial deployment to set up the required resources (Lambda function, ECR, IAM roles, and CodePipeline). This can be done by running the following command from the project’s root directory:

```shell
cdk deploy
```

This command will:

- Set up the Lambda function to run the Docker image.
- Configure AWS CodePipeline to automatically deploy updates whenever code is committed to the repository.
- Create necessary roles and permissions for Lambda, Docker, and CodePipeline.

**Continuous Deployment via CodePipeline**

Once the initial deployment is complete, any future commits to the main branch will automatically trigger the CI/CD pipeline. AWS CodePipeline will:

- Build the Docker image.
- Push the image to AWS ECR.
- Deploy the updated Lambda function with the latest Docker image.

You do not need to run `cdk deploy` manually after this, as the pipeline will handle future deployments automatically.

