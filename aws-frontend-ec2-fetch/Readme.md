# EC2 Instances without DNS Mapping - Script Documentation

## Use Case

This script is particularly useful for identify EC2 instances with public IPs that do not have corresponding DNS records, specifically for those instances that are expected to have DNS entries (e.g., front-end servers).

## Prerequisites

1. **Python Libraries**: Install the required Python libraries:
   - `boto3` - AWS SDK for Python to interact with AWS services.
   - `pandas` - For handling data and exporting to Excel.
   - `openpyxl` - For saving DataFrames as Excel files.

   Install these dependencies via pip:
   ```bash
   pip install boto3 pandas openpyxl
   ```
## Script Execution

### Step 1: Setting Up EC2 Connections

- The script establishes EC2 resource connections for multiple regions (`us-east-1`, `ap-south-1`, `us-west-2`).
- It uses Boto3's `ec2.resource` to interact with EC2 resources.

### Step 2: Fetching Route 53 DNS Records

- The script interacts with Route 53 via Boto3's `route53.client`.
- It retrieves all DNS records for the hosted zone `example.com` and stores the IP addresses associated with `A` records.

### Step 3: Identifying Mismatched Instances

- The script iterates through each EC2 instance in the specified regions and checks if the instance has a public IP.
- It compares the public IP addresses with the list of IP addresses fetched from Route 53 DNS records.
- If the IP address is not found in the DNS records and the instance name contains the substring `-frontend`, the instance is considered mismatched.
  
### Step 4: Storing Mismatched Instances

- The mismatched instances (with `-frontend` in the instance name but no DNS record) are appended to a list, which is then written to an Excel file (`No_DNS_EC2.xlsx`).
  
### Step 5: Generating Excel Output

- The mismatched instances are stored in a Pandas DataFrame and saved as an Excel file with the following columns:
  - `Instance ID`: EC2 instance ID.
  - `Instance Name`: EC2 instance name (tagged as 'Name').
  - `Public IP Address`: The public IP of the EC2 instance.
  - `Region`: The AWS region where the EC2 instance is located.

## Output File

The output file is an Excel sheet named `No_DNS_EC2.xlsx`. The sheet will contain the following columns:

| Instance ID | Instance Name  | Public IP Address | Region |
|-------------|----------------|-------------------|--------|
| i-axbbbbxbb | xyz-frontend   | 00.00.00.00       | us-west-2 |
| i-byaaaayaa | ab-frontend-ec2| 00.00.00.00       | us-east-1 |

  