import boto3
import csv

# List of allowed regions
ALLOWED_REGIONS = [
    'us-east-1',
    'us-east-2',
    'us-west-1',
    'us-west-2',
    'ap-south-1',
    'ap-northeast-3',
    'ap-northeast-2',
    'ap-northeast-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'ca-central-1',
    'eu-central-1',
    'eu-west-1',
    'eu-west-2',
    'eu-west-3',
    'eu-north-1',
    'sa-east-1'
]

def get_resources_without_tags(region):
    """Get resources without the 'test' tag and without any tags in a specific region."""
    session = boto3.Session(region_name=region)
    resource_groups_client = session.client('resourcegroupstaggingapi')

    resources = []
    paginator = resource_groups_client.get_paginator('get_resources')
    
    for page in paginator.paginate():
        for resource in page['ResourceTagMappingList']:
            resource_arn = resource['ResourceARN']
            tags = resource['Tags']
            # Check if there are no tags or if the 'test' tag is not present
            if not tags or all(tag['Key'] != 'test' for tag in tags):
                resources.append({
                    'ResourceType': resource_arn.split(':')[5],
                    'ResourceId': resource_arn,
                    'Region': region,
                    'Tags': tags
                })

    return resources

def write_to_csv(resource_list, filename='aws_resources_without_test_tag.csv'):
    """Write the resource list to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ResourceType', 'ResourceId', 'Region', 'Tags'])
        for resource in resource_list:
            tags = ', '.join(f"{tag['Key']}={tag['Value']}" for tag in resource['Tags'])
            writer.writerow([resource['ResourceType'], resource['ResourceId'], resource['Region'], tags])

def main():
    all_resources = []
    
    for region in ALLOWED_REGIONS:
        print(f"Fetching resources from region: {region}")
        resources = get_resources_without_tags(region)
        all_resources.extend(resources)

    write_to_csv(all_resources)

if __name__ == "__main__":
    main()