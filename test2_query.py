import requests

url = "http://127.0.0.1:8000/query"
headers = {"X-User-Id": "user2"}
data = {"question": "Do I have any upcoming travel plans?"}

resp = requests.post(url, headers=headers, json=data, timeout=180)

print("Status code:", resp.status_code)
print("Raw response:")
print(resp.text)

try:
    print("\nParsed JSON:")
    print(resp.json())
except Exception:
    print("Response was not valid JSON")
