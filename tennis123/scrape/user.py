import requests

# Constants
URL = "https://www.tennis123.net/search/searchUser"  # Change to the actual URL if different
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_user_id(username):
    """Send a POST request to search for the user and return the user ID if found."""
    payload = {"userName": username}
    response = requests.post(URL, headers=HEADERS, data=payload)

    if response.status_code == 200:
        response_data = response.json()
        if len(response_data["rows"]) == 0:
            print("User not found.")
            return None
        elif len(response_data["rows"]) > 1:
            print("Multiple users found. Please refine your search.")
            return None
        else:
            return response_data["rows"][0]["Uid"]
    else:
        print("Failed to retrieve data: ", response.status_code)
        return None
