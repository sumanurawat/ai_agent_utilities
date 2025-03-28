import os
import requests
from utils import get_cloudrun_url
# Get the URL using our helper function
CLOUDRUN_URL = get_cloudrun_url()

def call_with_get(name="YourName"):
    """Call the CloudRun service using GET request with query parameters"""
    response = requests.get(f"{CLOUDRUN_URL}/", params={"name": name})
    return response.text

def call_with_post(name="YourName", message="Welcome"):
    """Call the CloudRun service using POST request with JSON data"""
    response = requests.post(
        f"{CLOUDRUN_URL}/greet", 
        json={"name": name, "message": message}
    )
    return response.json()

if __name__ == "__main__":
    # Example usage
    print("Testing GET request:")
    print(call_with_get("Friend"))
    
    print("\nTesting POST request:")
    print(call_with_post("Friend", "Greetings"))