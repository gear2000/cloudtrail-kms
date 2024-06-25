variable "aws_default_region" {
  description = "The AWS region where the resources will be deployed. The default is 'us-east-1'."
  default     = "us-east-1"
}

variable "retention_in_days" {
  description = "The number of days to retain the logs for the Lambda function. The default is 1 day."
  default     = 1
}

variable "function_name" {
  description = "The name of the Lambda function."
  type        = string
}

variable "memory_size" {
  description = "The amount of memory in MB to allocate to the Lambda function. The default is 128 MB."
  default     = 128
  type        = number
}

variable "timeout" {
  description = "The maximum time in seconds that the Lambda function is allowed to run. The default is 3 seconds."
  default     = 300
  type        = number
}

variable "function_handler" {
  description = "The name of the function handler (the function in your code that Lambda calls to start executing your code)."
  type        = string
}

variable "runtime" {
  description = "The runtime environment for the Lambda function (e.g., 'python3.9', 'nodejs14.x', 'java11')."
  type        = string
  default     = "python3.9"
}

variable "s3_key" {
  description = "The path to the Lambda function code in the S3 bucket."
  type        = string
}

variable "s3_bucket" {
  description = "The name of the S3 bucket where the Lambda function code is stored."
  type        = string
}