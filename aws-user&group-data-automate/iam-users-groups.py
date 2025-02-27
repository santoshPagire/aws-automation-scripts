import boto3
import pandas as pd

def fetch_iam_groups():
    iam = boto3.client('iam')
    groups = iam.list_groups()['Groups']
    
    group_details = []
    for group in groups:
        group_name = group['GroupName']
        group_description = group.get('Description', 'No description available')
        policies = iam.list_attached_group_policies(GroupName=group_name)['AttachedPolicies']
        privileges = [policy['PolicyName'] for policy in policies]
        
        group_details.append({
            'Group name': group_name,
            'Description': group_description,
            'List of privileges': ', '.join(privileges)
        })

    return group_details

def fetch_iam_users():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']
    
    users_without_console_access = []
    group_wise_users = {}
    users_without_group = []

    for user in users:
        user_name = user['UserName']
        user_groups = iam.list_groups_for_user(UserName=user_name)['Groups']
        group_names = [group['GroupName'] for group in user_groups]
        
        # Check if the user belongs to any group
        if not group_names:
            users_without_group.append(user_name)

        # Default console login status is "Disabled"
        console_login_status = 'Disabled'
        try:
            # Check if user has a console login profile
            iam.get_login_profile(UserName=user_name)
            # If console access exists, check if the user has logged in
            console_login_status = 'Inactive'
            if user.get('PasswordLastUsed'):
                console_login_status = 'Active'
        except iam.exceptions.NoSuchEntityException:
            # If user doesn't have a login profile, their status is "Disabled"
            console_login_status = 'Disabled'
        
        access_keys = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
        
        aws_key_status = [key['Status'] for key in access_keys]
        
        # Get the descriptions of the access keys using list_user_tags
        aws_key_descriptions = []
        try:
            # Fetch tags associated with the user 
            tags_response = iam.list_user_tags(UserName=user_name)
            
            # Look for tags where the key is the Access Key ID
            for key in access_keys:
                access_key_id = key['AccessKeyId']
                description_tag = 'No description available'
                
                for tag in tags_response['Tags']:
                    if tag['Key'] == access_key_id:  
                        description_tag = tag['Value']  
                        break
                
                aws_key_descriptions.append(description_tag)
        except iam.exceptions.NoSuchEntityException:
            aws_key_descriptions.append('No description available')

        # Get the list of privileges for each user
        user_privileges = []
        for group in user_groups:
            policies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']
            user_privileges.extend([policy['PolicyName'] for policy in policies])
        
        user_info = {
            'List of users': user_name,
            'Status - Console login': console_login_status,
            'Status - AWS keys': ', '.join(aws_key_status) if aws_key_status else 'Not enabled',
            'Purpose of AWS keys': ', '.join(aws_key_descriptions) if aws_key_descriptions else 'No description available'
        }

        # Add user info under their respective group names
        for group in group_names:
            if group not in group_wise_users:
                group_wise_users[group] = []
            group_wise_users[group].append(user_info)
        
        # Add users without console access to a separate list
        if console_login_status == 'Disabled':
            users_without_console_access.append({
                'List of users': user_name,
                'List of privileges': ', '.join(user_privileges) if user_privileges else 'No privileges',
                'Status - Console login': console_login_status,
                'Status - AWS keys': ', '.join(aws_key_status) if aws_key_status else 'Not enabled',
                'Purpose of AWS keys': ', '.join(aws_key_descriptions) if aws_key_descriptions else 'No description available'
            })

    # Format the user data for the grouped output
    grouped_user_details = []
    for group_name, users_info in group_wise_users.items():
        for i, user_info in enumerate(users_info):
            if i == 0:
                # For the first user, include the group name and user in the first row
                grouped_user_details.append({
                    'Group name': group_name,
                    'List of users': user_info['List of users'],
                    'Status - Console login': user_info['Status - Console login'],
                    'Status - AWS keys': user_info['Status - AWS keys'],
                    'Purpose of AWS keys': user_info['Purpose of AWS keys']
                })
            else:
                # For subsequent users, leave the "Group name" blank and only include user details
                grouped_user_details.append({
                    'Group name': '',
                    'List of users': user_info['List of users'],
                    'Status - Console login': user_info['Status - Console login'],
                    'Status - AWS keys': user_info['Status - AWS keys'],
                    'Purpose of AWS keys': user_info['Purpose of AWS keys']
                })
    
    # Now also include users who are not part of any group
    for user_name in users_without_group:
        # Fetch user details for users without groups
        user_groups = iam.list_groups_for_user(UserName=user_name)['Groups']
        group_names = [group['GroupName'] for group in user_groups]

        # Default console login status is "Disabled"
        console_login_status = 'Disabled'
        try:
            # Check if user has a console login profile
            iam.get_login_profile(UserName=user_name)
            # If console access exists, check if the user has logged in
            console_login_status = 'Inactive'
            if user.get('PasswordLastUsed'):
                console_login_status = 'Active'
        except iam.exceptions.NoSuchEntityException:
            # If user doesn't have a login profile, their status is "Disabled"
            console_login_status = 'Disabled'
        
        access_keys = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
        aws_key_status = [key['Status'] for key in access_keys]
        
        # Get the descriptions of the access keys using list_user_tags
        aws_key_descriptions = []
        try:
            # Fetch tags associated with the user
            tags_response = iam.list_user_tags(UserName=user_name)
            
            # Look for tags where the key is the Access Key ID
            for key in access_keys:
                access_key_id = key['AccessKeyId']
                description_tag = 'No description available'
                
                for tag in tags_response['Tags']:
                    if tag['Key'] == access_key_id:  
                        description_tag = tag['Value']  
                        break
                
                aws_key_descriptions.append(description_tag)
        except iam.exceptions.NoSuchEntityException:
            aws_key_descriptions.append('No description available')

        # Get the list of privileges for each user
        user_privileges = []
        for group in user_groups:
            policies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']
            user_privileges.extend([policy['PolicyName'] for policy in policies])

        user_info = {
            'Group name': 'NA',
            'List of users': user_name,
            'Status - Console login': console_login_status,
            'Status - AWS keys': ', '.join(aws_key_status) if aws_key_status else 'Not enabled',
            'Purpose of AWS keys': ', '.join(aws_key_descriptions) if aws_key_descriptions else 'No description available'
        }

        grouped_user_details.append(user_info)
    
    return grouped_user_details, users_without_console_access

def save_to_excel(group_data, user_data, users_without_console_access, filename='iam_details.xlsx'):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        pd.DataFrame(group_data).to_excel(writer, sheet_name='Groups', index=False)
        pd.DataFrame(user_data).to_excel(writer, sheet_name='Users', index=False)
        pd.DataFrame(users_without_console_access).to_excel(writer, sheet_name='Users without Console Access', index=False)

def main():
    group_data = fetch_iam_groups()
    user_data, users_without_console_access = fetch_iam_users()
    save_to_excel(group_data, user_data, users_without_console_access)
    print("Data is added in excel sheet")

if __name__ == "__main__":
    main()
