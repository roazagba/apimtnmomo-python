import argparse
from .sandbox_user_provisioning import SandboxUserProvisioning
from .utilities import Helpers
import json

def main():
    parser = argparse.ArgumentParser(description='Creates a Momo API user in the sandbox environment')
    parser.add_argument('baseurl', type=str, help='Base URL for the API')
    parser.add_argument('primarykey', type=str, help='Primary Key for the API')
    parser.add_argument('callbackurl', type=str, help='Callback URL for the API')

    args = parser.parse_args()

    print('Creating API and API Key Secrete user with the following details:')
    print(f"Base URL: {args.baseurl}")
    print(f"Primary Key: {args.primarykey}")
    print(f"Callback URL: {args.callbackurl}")

    try:
        user = SandboxUserProvisioning({
            'baseURL': args.baseurl,
            'userID': Helpers.uuid4(),
            'primaryKey': args.primarykey,
            'providerCallbackHost': args.callbackurl
        })
        result = user.create()
        print("API User and API Key Secrete created successfully.")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error creating API user: {e}")

if __name__ == '__main__':
    main()
