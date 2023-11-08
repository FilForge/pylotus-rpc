import os

def parse_fullnode_api_info():
    # Try to fetch the environment variable
    fullnode_api_info = os.environ.get("FULLNODE_API_INFO")
    lotus_token = os.environ.get("LOTUS_RPC_TOKEN")

    # If it's not found, raise an error
    if not fullnode_api_info:
        raise EnvironmentError("FULLNODE_API_INFO environment variable is not set.")
    
    # Split the info at the ':' to separate JWT token and address
    jwt_token, address = fullnode_api_info.split(":", 1)

    # Extract the host by splitting the address string and taking the appropriate section
    parts = address.split("/")
    port = parts[4]
    host = parts[2]
    
    return {
        "jwt_token": jwt_token,
        "host": host,
        "port": port
    }