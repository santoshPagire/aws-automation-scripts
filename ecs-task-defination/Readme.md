
# ECS Service Environment Variable Fetcher

This Python script retrieves information about a specific ECS (Elastic Container Service) service named "demo-app-service" from all ECS clusters in the specified AWS region. It extracts the task definition ARN associated with the service and the value of a specific environment variable (with the key "Name") from that task definition. The results are saved to a CSV file.


### Main Functionality

- **List Clusters**: The script lists all ECS clusters in the specified region (`us-west-2`).
- **List Services**: For each cluster, it retrieves all services and checks for the presence of specific service. e.g:"demo-app-service".
- **Describe Service**: If the service is found, it retrieves the task definition associated with that service.
- **Extract Environment Variable**: The script extracts the value of the environment variable with the specific key (e.g:"Name") from the task definition.
- **Write to CSV**: The results are written to a CSV file.

## Example Output

The generated `ecs_details.csv` file will look like this:

### Example Output Table

| Cluster Name     | Service Name                | Task Definition ARN                                      |  Env Value |
|-------------------|-----------------------------|---------------------------------------------------------|---------------------|
| test-cluster-1    | demo-app-service     | arn:aws:ecs:us-west-2:123456789012:task-definition/demo-app:1 | production          |
| test-cluster-2    | demo-app-service     | arn:aws:ecs:us-west-2:123456789012:task-definition/demo-app:2 | staging             |      |
