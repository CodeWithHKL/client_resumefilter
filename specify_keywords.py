import requests

url = "http://127.0.0.1:8000/rank-resumes"

# Update this line to include the specific keywords you want
skills = "SQL, engineer" 

files = [
    ('files', open('Resume202404280938.pdf', 'rb'))
]

response = requests.post(url, data={'skills': skills}, files=files)
print(response.json())