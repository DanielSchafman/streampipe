from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class Connection(BaseModel):
    name: str
    plugin: str
    access_key: str = None
    secret_key: str = None
    regions: str = None
    project_id: str = None
    credentials_file: str = None
    client_id: str = None
    client_secret: str = None
    tenant_id: str = None
    subscription_id: str = None

# In-memory storage for connections (you might want to use a database instead)
connections = {}

@router.post("/connections/")
async def add_connection(connection: Connection):
    if connection.name in connections:
        raise HTTPException(status_code=400, detail="Connection already exists")

    connections[connection.name] = connection
    write_connection_to_file(connection)  # Function to write the connection to the config file
    return {"message": "Connection added successfully"}

@router.delete("/connections/{connection_name}")
async def remove_connection(connection_name: str):
    if connection_name not in connections:
        raise HTTPException(status_code=404, detail="Connection not found")

    del connections[connection_name]
    remove_connection_from_file(connection_name)  # Function to remove the connection from the config file
    return {"message": "Connection removed successfully"}

@router.get("/connections/")
async def list_connections():
    return {"connections": list(connections.values())}

def write_connection_to_file(connection: Connection):
    steampipe_config_dir = "/home/steampipeuser/.steampipe/config"
    
    # Ensure the directory exists before writing the config file
    os.makedirs(steampipe_config_dir, exist_ok=True)

    config_content = f"""
connection "{connection.name}" {{
  plugin    = "{connection.plugin}"
"""
    if connection.plugin == "aws":
        config_content += f"""
  access_key = "{connection.access_key}"
  secret_key = "{connection.secret_key}"
  regions    = ["{connection.regions}"]
}}
"""
    elif connection.plugin == "gcp":
        config_content += f"""
  project   = "{connection.project_id}"
  credentials_file = "{connection.credentials_file}"
}}
"""
    elif connection.plugin == "azure":
        config_content += f"""
  client_id = "{connection.client_id}"
  client_secret = "{connection.client_secret}"
  tenant_id = "{connection.tenant_id}"
  subscription_id = "{connection.subscription_id}"
}}
"""
    # Write or append to the configuration file
    with open(f"{steampipe_config_dir}/cloud.spc", "a") as config_file:
        config_file.write(config_content)

def remove_connection_from_file(connection_name: str):
    # This function should handle the removal of the specified connection
    steampipe_config_dir = "/home/steampipeuser/.steampipe/config"
    with open(f"{steampipe_config_dir}/cloud.spc", "r") as file:
        lines = file.readlines()

    with open(f"{steampipe_config_dir}/cloud.spc", "w") as file:
        skip = False
        for line in lines:
            if f'connection "{connection_name}"' in line:
                skip = True  # Skip the next lines until we reach the closing bracket
            if line.strip() == "}" and skip:
                skip = False  # Stop skipping when we reach the closing bracket
                continue  # Skip the closing bracket line
            if not skip:
                file.write(line)
