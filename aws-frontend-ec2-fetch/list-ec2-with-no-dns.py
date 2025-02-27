import boto3
import pandas as pd

# Set up EC2 resource connections for all regions
ec2_resources = {}
regions = ['us-east-1', 'ap-south-1', 'us-west-2']     
for region in regions:
    ec2_resources[region] = boto3.resource('ec2', region_name=region)

# Set Route 53 client
route53 = boto3.client('route53')                   

zone_name = 'example.com'
response = route53.list_hosted_zones_by_name(DNSName=zone_name)
hosted_zone_id = response['HostedZones'][0]['Id']

#Pagination for Route 53 record sets
record_ips = []
next_record_set = None
while True:
    # Fetch the record sets
    if next_record_set:
        response = route53.list_resource_record_sets(HostedZoneId=hosted_zone_id, StartRecordName=next_record_set)
    else:
        response = route53.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    
    # Extract the IPs
    for record_set in response['ResourceRecordSets']:
        if record_set['Type'] == 'A' and 'ResourceRecords' in record_set:
            record_ips.extend([record['Value'] for record in record_set['ResourceRecords']])
    
    # Check if there are more records to fetch
    next_record_set = response.get('NextRecordName')
    if not next_record_set:
        break


no_dns_instances = []

for region in regions:
    ec2 = ec2_resources[region]
    paginator = ec2.meta.client.get_paginator('describe_instances')
    for page in paginator.paginate():
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                if 'PublicIpAddress' in instance:
                    public_ip = instance['PublicIpAddress']
                    if public_ip not in record_ips:
                        instance_name = ''
                        if 'Tags' in instance:
                            for tag in instance['Tags']:
                                if tag['Key'] == 'Name':
                                    instance_name = tag['Value']
                                    break
                        
                        if "-front" in instance_name:
                            no_dns_instances.append((instance['InstanceId'], instance_name, public_ip, region))

# Create a pandas DataFrame from the mismatched instances list
df = pd.DataFrame(no_dns_instances, columns=['Instance ID', 'Instance Name', 'Public IP Address', 'Region'])
excel_file = 'No_DNS_EC2.xlsx'
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Instances with '-front' in their Name but no DNS record have been written to {excel_file}")
