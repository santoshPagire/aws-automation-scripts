import boto3
import csv

def main():
    ecs_client = boto3.client('ecs', region_name='us-west-2')

    clusters_response = ecs_client.list_clusters()
    cluster_arns = clusters_response['clusterArns']

    print(f"Clusters found: {cluster_arns}")

    with open('ecs_details.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Cluster Name', 'Service Name', 'Task Definition ARN', 'Vpc Endpoint Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for cluster_arn in cluster_arns:
            service_arns = list_all_services(ecs_client, cluster_arn)
            print(f"Services in cluster {cluster_arn}: {service_arns}")

            # Check if the specific service is present
            for service_arn in service_arns:
                if 'demo-app-service' in service_arn:
                   
                    service_details = ecs_client.describe_services(cluster=cluster_arn, services=[service_arn.split('/')[-1]])
                    service_info = service_details['services'][0]

                
                    task_definition_arn = service_info['taskDefinition']
                    service_name = service_arn.split('/')[-1]

                    
                    task_definition_details = ecs_client.describe_task_definition(taskDefinition=task_definition_arn)
                    container_definitions = task_definition_details['taskDefinition']['containerDefinitions']

                    env_var_value = None

                    # Loop through container definitions to find the environment variable
                    for container in container_definitions:
                        for env in container.get('environment', []):
                            if env['name'] == 'Name':  # Check the specific environment variable key
                                env_var_value = env['value']
                                break
                        if env_var_value is not None:
                            break  

                    cluster_name = cluster_arn.split('/')[-1]

                    # Write the data to the CSV file
                    writer.writerow({
                        'Cluster Name': cluster_name,
                        'Service Name': service_name,
                        'Task Definition ARN': task_definition_arn,
                        'Vpc Endpoint Value': env_var_value
                    })
                    break  
            else:
                print(f"Service 'demo-app-service' not found in cluster {cluster_arn}")

def list_all_services(ecs_client, cluster_arn):
    service_arns = []
    next_token = None

    while True:
        if next_token:
            response = ecs_client.list_services(cluster=cluster_arn, nextToken=next_token)
        else:
            response = ecs_client.list_services(cluster=cluster_arn)

        service_arns.extend(response['serviceArns'])

        next_token = response.get('nextToken')
        if not next_token:
            break

    return service_arns

if __name__ == "__main__":
    main()

print(f"Data added in csv file")