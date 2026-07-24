import os
import boto3


if __name__ == "__main__":
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    session = boto3.session.Session(region_name=region)
    client = session.client("sts")

    response = client.get_caller_identity()
    print("AWS SDK configured successfully")
    print(f"Account: {response.get('Account')}")
    print(f"Arn: {response.get('Arn')}")
    print(f"UserId: {response.get('UserId')}")
