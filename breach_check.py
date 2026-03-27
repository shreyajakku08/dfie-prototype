import requests
import os

def check_breaches(email):
    """
    Check if an email has been in any data breaches using HaveIBeenPwned API.
    If the API fails (e.g. no API key, rate limit), use mock fallback data.
    """
    # Optional: Get API key from environment if you have one
    api_key = os.environ.get('HIBP_API_KEY', '') 
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    
    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'DFIE-Hackathon-Prototype'
    }
    
    try:
        if not api_key:
            # Skip actual API call and jump straight to mock data if no key is provided
            # (Since HIBP now strictly requires a paid API key)
            raise ValueError("No API Key provided")
            
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # 404 means no breaches found for this email
            return []
        else:
            # Fallback for unexpected status codes (401 Unauthorized, 429 Rate Limit, etc.)
            raise requests.exceptions.HTTPError(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Breach check API failed ({e}). Using mock fallback data.")
        return get_mock_breach_data(email)

def get_mock_breach_data(email):
    """
    Returns mock data for testing purposes or when the API fails.
    """
    # Simple logic: 'clean@example.com' returns no breaches, anything else gets the mock data.
    if email.lower() == 'clean@example.com':
        return []
        
    return [
        {
            "Name": "Mockbook",
            "Title": "Mockbook Social Network",
            "Domain": "mockbook.com",
            "BreachDate": "2021-04-01",
            "Description": "In April 2021, a huge database of user data was scraped and shared online containing names, emails, and phone numbers.",
            "DataClasses": ["Email addresses", "Names", "Phone numbers", "Passwords"]
        },
        {
            "Name": "FakeFit",
            "Title": "FakeFit Fitness App",
            "Domain": "fakefit.app",
            "BreachDate": "2023-11-15",
            "Description": "Hackers gained access to fitness records and email addresses of millions of users.",
            "DataClasses": ["Email addresses", "Health data", "Passwords"]
        }
    ]

# For testing this script independently
if __name__ == "__main__":
    print(check_breaches("test@example.com"))
