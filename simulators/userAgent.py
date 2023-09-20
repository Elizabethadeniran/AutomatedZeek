import requests
import random

def simulate_user_agent():
    # Define the URL of the web server you want to send the request to
    url = "http://127.0.0.1:9541/agents"  # Replace with the actual URL

    # Define the custom User-Agent string
    custom_user_agent = [
        "AppleWebKit/537.36 (KHTML, like Gecko)",
        "Chrome/111.0.0.0",
        "Edg/111.0.1661.41",
        "MyCustomUserAgent/1.0",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "OPR/102.0.0.0",
        "Safari/537.36"
    ]

    # Define the headers with the custom User-Agent
    headers = {
        "User-Agent": random.choice(custom_user_agent)
    }

    try:
        # Send the HTTP request with the custom User-Agent
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            print("Request was successful.")
        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


    


if __name__ == '__main__':
    for x in range(500):
        simulate_user_agent()
