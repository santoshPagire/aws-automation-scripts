import boto3
from datetime import datetime, timedelta
import csv
import pytz

# Configuration appsync-dynamodb
TARGET_BUCKETS = ["cost-and-usage-reports-baeced90", "random-test-bucket"]
OUTPUT_FILE = "bucket_sizes_30days.csv"
TIMEZONE = pytz.utc

def get_bucket_region(bucket_name):
    """Get the AWS region for a specific bucket"""
    try:
        region = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        return region if region is not None else 'us-east-1'
    except Exception as e:
        print(f"Error getting region for {bucket_name}: {str(e)}")
        return 'us-east-1'

def get_last_30_days():
    """Generate list of dates for the last 30 days in YYYY-MM-DD format"""
    now = datetime.now(TIMEZONE)
    return [(now - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]

def get_bucket_size(bucket_name, cloudwatch):
    """Fetch bucket size metrics from CloudWatch across all storage classes"""
    storage_classes = [
        'StandardStorage',
        'IntelligentTieringFAStorage',
        'IntelligentTieringIAStorage',
        'GlacierStorage',
        'DeepArchiveStorage'
    ]

    size_data = {}
    end_time = datetime.now(TIMEZONE)
    start_time = end_time - timedelta(days=31)  # 31 days back to ensure 30-day coverage

    for storage_type in storage_classes:
        try:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': storage_type}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Average'],
                Unit='Bytes'
            )

            for dp in response['Datapoints']:
                date = dp['Timestamp'].astimezone(TIMEZONE).strftime('%Y-%m-%d')
                current_size = dp['Average']/ (1024 * 1024)
                if date in size_data:
                    size_data[date] += current_size
                else:
                    size_data[date] = current_size

        except Exception as e:
            print(f"Error processing {storage_type} for {bucket_name}: {str(e)}")
            continue

    return size_data

def generate_report():
    """Generate the CSV report for 30 days"""
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = None
        dates = get_last_30_days()

        for bucket in TARGET_BUCKETS:
            try:
                # Get bucket-specific region
                region = get_bucket_region(bucket)
                
                # Create region-specific clients
                cloudwatch = boto3.client('cloudwatch', region_name=region)

                print(f"Processing bucket: {bucket} in region: {region}")
                
                # Get size data
                size_data = get_bucket_size(bucket, cloudwatch)
                
                # Prepare row data
                row = {'Bucket Name': bucket, 'AWS Region': region}
                for date in dates:
                    size = size_data.get(date, 0)
                    row[date] = round(size, 2) if size > 0 else 'N/A'

                # Initialize writer with header
                if not writer:
                    fieldnames = ['Bucket Name', 'AWS Region'] + dates
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

                writer.writerow(row)

            except Exception as e:
                print(f"Failed to process bucket {bucket}: {str(e)}")
                continue

    print(f"30-day report generated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    s3 = boto3.client('s3')
    generate_report()