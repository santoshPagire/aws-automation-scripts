# README

## Overview

This Python script interacts with AWS Resource Groups Tagging API to fetch resources that are tagged with a specific key-value pair, and then adds a new tag (`awsApplication`) to those resources.

## Setup Instructions

### 1. Install dependencies

Install `boto3` using following command:

```bash
pip install boto3
```

### 2. Set up your AWS credentials

* **1. Using Environment variables:**
  Set the AWS credentials and region as environment variables:
  ```bash
  export AWS_ACCESS_KEY_ID=your_access_key
  export AWS_SECRET_ACCESS_KEY=your_secret_key
  export AWS_REGION=your_aws_region
  ```
* **2. AWS CLI configuration:**
  Use following command to configure aws credentials.
  ```bash
  aws configure
  ```

### 3. Set the environment variables for the script

Before running the script,You need to export below environment variables:

* **`AWS_REGION`** : AWS region where the resources are located (e.g., `us-east-1`, `us-west-2`).
* **`TAG_KEY`** : The key of the tag you want to filter resources by (e.g., `Environment`).
* **`TAG_VALUE`** : The value of the tag you want to filter resources by (e.g., `Production`).
* **`AWS_APPLICATION_ARN`** : The value for the new tag (`awsApplication`) to be added to the resources.

Example:

```bash
export AWS_REGION="us-east-1"
export TAG_KEY="Environment"
export TAG_VALUE="Production"
export AWS_APPLICATION_ARN="arn:aws:elasticbeanstalk:us-east-1:123456789012:application/MyApplication"
```

### 4. Running the Script

```bash
python application_tagging.py
```

## Example Output

```bash
Checking resources in region: us-east-1
Successfully tagged resource: arn:aws:s3:::example-bucket
Resource already tagged: arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef
Tagging completed successfully in us-east-1. Tagged 3 resources.
```
