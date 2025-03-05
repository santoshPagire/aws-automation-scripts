import boto3
import csv

ecs_client = boto3.client('ecs', region_name='ap-south-1')

with open('ecs_task_definitions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(['Cluster Name', 'Vpc Endpoint'])

    response = ecs_client.list_clusters()
    cluster_arns = response['clusterArns']
    for cluster_arn in cluster_arns:
        # Extract the cluster name from the ARN
        cluster_name = cluster_arn.split('/')[-1]
        print(f"Checking cluster: {cluster_name}")

        services_response = ecs_client.list_services(cluster=cluster_name)
        service_arns = services_response['serviceArns']

        found_test_service = False
        for service_arn in service_arns:
            # Extract the service name from the ARN
            service_name = service_arn.split('/')[-1]
            print(f"Service found: {service_name}") 
            if service_name == 'Test-service':
                found_test_service = True
                break  

        if not found_test_service:
            print(f"Service 'Test-service' not found in cluster: {cluster_name}. Skipping...")
            continue  

        # List task definitions for the current cluster
        task_definitions_response = ecs_client.list_task_definitions(
            status='ACTIVE'
        )
        
        task_definitions = task_definitions_response['taskDefinitionArns']
        
        for task_definition_arn in task_definitions:
            print(f"Checking task definition: {task_definition_arn}")
            
            # Get the task definition details
            task_definition_response = ecs_client.describe_task_definition(
                taskDefinition=task_definition_arn
            )
            
            task_definition = task_definition_response['taskDefinition']
            
            # Extract the environment variables and check for "Name"
            for container in task_definition['containerDefinitions']:
                for env_var in container.get('environment', []):
                    if env_var['name'] == 'Name':
            
                        writer.writerow([cluster_name, env_var['value']])
