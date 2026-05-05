import requests

URL = "http://127.0.0.1:8000"

def test_get_root():
    response = requests.get(URL)
    if response.status_code == 400:
        print("GET / - Success")
    else:
        print("GET / - Failed")


if __name__ == "__main__":
    test_get_root()