import requests
from utils import get_cloudrun_url

url = get_cloudrun_url()

def generate_text(prompt):
    """Generate text using the Cloud Run LLM endpoint"""
    response = requests.post(
        f"{url}/generate",
        json={"prompt": prompt}
    )
    return response.json()

# Example usage
result = generate_text("Explain quantum computing to me in simple terms")
print(result)