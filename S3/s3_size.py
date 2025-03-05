import boto3
import pandas as pd

def get_s3_buckets_and_sizes():
    session = boto3.Session()
    s3 = session.client('s3')

    response = s3.list_buckets()
    buckets = response['Buckets']

    # Initialize a dictionary to hold bucket sizes
    bucket_sizes = {}

    for bucket in buckets:
        bucket_name = bucket['Name']
        print(f"Calculating size for bucket: {bucket_name}")

        total_size = 0

        # List objects in the bucket
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name):
            if 'Contents' in page:
                for obj in page['Contents']:
                    total_size += obj['Size']

    
        total_size_mb = total_size / (1024 * 1024) 

        total_size_mb = round(total_size_mb, 2)

        # Store the size in the dictionary
        bucket_sizes[bucket_name] = total_size_mb

    return bucket_sizes

def save_to_csv(bucket_sizes, filename='s3_bucket_sizes_mb.csv'):
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(list(bucket_sizes.items()), columns=['Bucket Name', 'Size (MB)'])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    bucket_sizes = get_s3_buckets_and_sizes()
    
    save_to_csv(bucket_sizes)