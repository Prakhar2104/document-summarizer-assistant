import requests

# URL of your local backend
url = "http://127.0.0.1:8000/upload/"

# Replace 'example.pdf' with your test file path
file_path = r"C:\Users\tiwar\OneDrive\Desktop\declarationform.jpg"

with open(file_path, "rb") as f:
    files = {"file": (r"C:\Users\tiwar\OneDrive\Desktop\declarationform.jpg", f)}
    response = requests.post(url, files=files)

print(response.json())
