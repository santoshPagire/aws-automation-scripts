# README: S3 Bucket Size Fetcher

This Python script retrieve the sizes of all S3 buckets in your AWS account and saves the information in a CSV file.

## Prerequisites

1. **Required Libraries** :

Install the required libraries, use pip:

```bash
pip install boto3 pandas
```

## Usage

1. **Clone or Download the Script** :
   Download or clone this script to your local machine.
```bash
git clone https://github.com/santoshPagire/aws_task.git
```
2. **Run the Script** :
   Open a terminal or command prompt and run the script using Python.

```bash
   python s3_size.py
```

## Output :
   The script will retrive buckets and its size.(`in MB`) after successfully run it prints below  message.

```bash
   Data saved to s3_bucket_sizes_mb.csv
```


