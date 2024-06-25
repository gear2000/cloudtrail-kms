# Introduction

This AWS Lambda function is designed to look up and retrieve Key Management Service (KMS) decryption events that have occurred within the last hour, based on the AWS CloudTrail logs. It assumes that CloudTrail has already been implemented and is actively recording events in the user's AWS account.

The function leverages the AWS SDK for Python (Boto3) to interact with the CloudTrail service. It first sets the time range for the event lookup, with the start time being one hour in the past and the end time being the current time. The function then initiates a CloudTrail client and uses the lookup_events method to retrieve the relevant KMS decryption events within the specified time period.

After gathering the CloudTrail events, the function processes the results and returns them as the body of the Lambda function response, with a status code of 200 to indicate successful execution.

# Run Locally

  ```
  python3.9 -m venv /tmp/venv3 
  source /tmp/venv3/bin/activate
  pip install -r src/requirements.txt 
  cd src
  python cloudtrail_kms.py 
  ```

# Deploy Lambda Function to AWS


-  Step 1 - To create and deploy the AWS Lambda function, follow these steps:

   - Build the Lambda function Docker image:
     Use the provided Dockerfile (Dockerfile-to-s3) to build the Docker image.

   - Deploy the Lambda function package:
     Start a temporary Docker container based on the previously built image.
     The running Docker container will automatically:
     Create a ZIP file containing the Lambda function code and dependencies.
     The name of the ZIP file will be $LAMBDA_PKG_NAME.zip, where $LAMBDA_PKG_NAME is a variable representing the desired name for the Lambda package.
     Upload the ZIP file to the correct S3 bucket and S3 key. The S3 key will be the same as the ZIP file name: $LAMBDA_PKG_NAME.zip.

   - This process leverages the provided Dockerfile and the functionality built into the Docker container to handle the creation and deployment of the Lambda function package. By automating these steps, the process can be easily integrated into a continuous integration/continuous deployment (CI/CD) pipeline.
     

   - example

     ``` example
     export DOCKER_TEMP_IMAGE=temp-lambda-pkg
     export DOCKERFILE_LAMBDA=Dockerfile-to-s3
     export AWS_ACCESS_KEY_ID=<access_key_id>
     export AWS_SECRET_ACCESS_KEY=<secret_access_key>
     export AWS_DEFAULT_REGION=us-east-1

     export S3_BUCKET=lambda-bucket-435345
     export LAMBDA_PKG_NAME=kms-decrypt  # s3_key is ${LAMBDA_PKG_NAME}.zip

     ./docker-to-lambda.sh

     ```


-  Step 2 - To deploy the AWS Lambda function using OpenTofu/Terraform, follow these steps:

   - Apply the OpenTofu/Terraform Configuration (terraform)
   The provided OpenTofu/Terraform configuration files will automatically:
   Create the SNS (Simple Notification Service) topic.
   Create the AWS Lambda function and configure it to be triggered by the SNS topic.
   Create the EventBridge (Amazon CloudWatch Events) rule to insert an empty JSON object into the SNS topic every hour, triggering the Lambda function on a scheduled basis.

   - Manually Invoke the Function:
   To manually trigger the Lambda function, you can publish a message to the SNS topic.
   This will cause the Lambda function to be invoked and process the message.

   - By using the pre-built OpenTofu/Terraform configuration, the deployment of the Lambda function, SNS trigger, and EventBridge schedule can be automated. This approach ensures consistency, maintainability, and easy management of the infrastructure through code.  

   - It is advisable to create a CI/CD pipeline for the OpenTofu/Terraform deploy that includes:
     - create remote backend to store terraform tfstate
     - create <terraform or env>.tfvars 
     - format Terraform files 
       - example 
       ```
       tofu fmt
       ```
     - evaluate security risks with tfsec and iterate Terraform code accordingly
       ```
       docker run --rm -it -v "$(pwd):/src" aquasec/tfsec /src
       ```
     - check into code
     - use secrets manager in the CI/CD system to inject AWS credentials or use a CI/CD system that can assume an IAM role (e.g. Gitlab runners)
     - initial deploy - (make to store tf plan file)
       ```
       tofu init
       tofu plan -out=tofu-kms.plan # store the plan file keep as reference (e.g. Gitlab artifact)
       tofo apply tofu-kms.plan
       ```
     - periodic checks for drift in CI/CD system
       ```
       tofu plan -detailed-exitcode
       ```
