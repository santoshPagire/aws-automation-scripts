import boto3
import os

# Exported Environment variables
AWS_REGION = os.getenv('AWS_REGION')
AWS_APPLICATION_ARN = os.getenv('AWS_APPLICATION_ARN')
TAG_KEY = os.getenv('TAG_KEY')
TAG_VALUE = os.getenv('TAG_VALUE')


def list_and_tag_resources():
    print(f"Checking resources in region: {AWS_REGION}")
    
    session = boto3.Session(region_name=AWS_REGION)
    resource_client = session.client('resourcegroupstaggingapi')

    tag_filters = {
        'TagFilters': [
            {
                'Key': TAG_KEY,
                'Values': [TAG_VALUE]
            }
        ]
    }

    tagged_resources = 0
    pagination_token = None

    while True:
        if pagination_token:
            tag_filters['PaginationToken'] = pagination_token

        # Get resources with the specified tag
        response = resource_client.get_resources(**tag_filters)

        resources = response.get('ResourceTagMappingList', [])

        for resource in resources:
            resource_arn = resource['ResourceARN']
            tags = {tag['Key']: tag['Value'] for tag in resource['Tags']}

            # Check if 'awsApplication' tag is present
            if 'awsApplication' not in tags:
                try:
                    resource_client.tag_resources(
                        ResourceARNList=[resource_arn],
                        Tags={'awsApplication': AWS_APPLICATION_ARN}
                    )
                    tagged_resources += 1
                    print(f"Successfully tagged resource: {resource_arn}")
                except Exception as e:
                    print(f"Failed to tag resource: {resource_arn}. Error: {str(e)}")
            else:
                print(f"Resource already tagged: {resource_arn}")

        # Check if there are more resources to fetch
        pagination_token = response.get('PaginationToken')
        if not pagination_token:
            break

    if tagged_resources > 0:
        print(f"Tagging completed successfully in {AWS_REGION}. Tagged {tagged_resources} resources.")
    else:
        print(f"No resources were tagged in {AWS_REGION}.")

if __name__ == "__main__":
    list_and_tag_resources()