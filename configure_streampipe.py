import os
import sys

# Initialize the configuration content
config_content = ""

# Check for AWS credentials
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-east-1')  # Default to us-east-1 if region is not specified

if aws_access_key and aws_secret_key:
    config_content += f"""
connection "aws_all" {{
  type        = "aggregator"
  plugin      = "aws"
  connections = ["aws_*"]
}}

connection "aws_{aws_region}" {{
  plugin    = "aws"
  access_key = "{aws_access_key}"
  secret_key = "{aws_secret_key}"
  region     = "{aws_region}"
}}
"""

# Check for GCP credentials
gcp_project_id = os.getenv('GCP_PROJECT_ID')
gcp_credentials_file = os.getenv('GCP_CREDENTIALS_FILE')

if gcp_project_id and gcp_credentials_file:
    config_content += f"""
connection "gcp" {{
  plugin    = "gcp"
  project   = "{gcp_project_id}"
  credentials_file = "{gcp_credentials_file}"
}}
"""

# Check for Azure credentials
azure_client_id = os.getenv('AZURE_CLIENT_ID')
azure_client_secret = os.getenv('AZURE_CLIENT_SECRET')
azure_tenant_id = os.getenv('AZURE_TENANT_ID')
azure_subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

if azure_client_id and azure_client_secret and azure_tenant_id and azure_subscription_id:
    config_content += f"""
connection "azure" {{
  plugin = "azure"
  client_id = "{azure_client_id}"
  client_secret = "{azure_client_secret}"
  tenant_id = "{azure_tenant_id}"
  subscription_id = "{azure_subscription_id}"
}}
"""

# Check if any configuration was generated
if not config_content.strip():
    print("No valid cloud credentials found. Please provide credentials for at least one cloud provider.")
    sys.exit(1)

# Ensure the directory exists before writing the config file
steampipe_config_dir = "/root/.steampipe/config"
os.makedirs(steampipe_config_dir, exist_ok=True)

# Write the configuration file to the Steampipe directory
with open(f"{steampipe_config_dir}/cloud.spc", "w") as config_file:
    config_file.write(config_content)

print("Steampipe configuration completed successfully.")