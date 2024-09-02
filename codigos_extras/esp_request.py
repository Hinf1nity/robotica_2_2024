import requests
import sys

def send_request(url, data):
    try:
        response = requests.get(f'http://{url}/{data}')
        print(response.text)
    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    url = sys.argv[1]
    data = sys.argv[2]
    send_request(url, data)