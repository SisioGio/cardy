import boto3
from botocore.exceptions import ClientError
import json
def get_secret(name,key=None, region_name="eu-central-1"):
    """
    Retrieve a secret value from AWS Secrets Manager.

    Args:
        name (str): The name or ARN of the secret.
        region_name (str): AWS region where the secret is stored.

    Returns:
        str: The secret value (as string). If the secret is JSON, parse it after retrieval.
    """
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=name)
    except ClientError as e:
        # Handle exceptions
        print(f"Error retrieving secret {name}: {e}")
        raise e

    # Secrets Manager can store either SecretString or SecretBinary
    if "SecretString" in get_secret_value_response:
        try:
            return json.loads(get_secret_value_response["SecretString"])
        except Exception as e:
            return get_secret_value_response["SecretString"]
    else:
        import base64
        return base64.b64decode(get_secret_value_response["SecretBinary"]).decode("utf-8")


