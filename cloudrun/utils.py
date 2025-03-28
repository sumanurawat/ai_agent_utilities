# Try to get URL from environment variable first, then from secrets file
import os
def get_cloudrun_url():
    # Check environment variable first
    url = os.environ.get("CLOUDRUN_URL")
    if url:
        return url
        
    # If not found in environment, try to import from secrets file
    try:
        from secret import CLOUDRUN_URL
        return CLOUDRUN_URL
    except (ImportError, AttributeError):
        try:
            # Try absolute import if relative import fails
            from secret import CLOUDRUN_URL
            return CLOUDRUN_URL
        except (ImportError, AttributeError):
            raise ValueError(
                "CLOUDRUN_URL not found. Please set it as an environment variable "
                "or create a secrets.py file with CLOUDRUN_URL defined."
            )
