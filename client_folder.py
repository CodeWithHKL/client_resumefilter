import requests
import os

# 1. Configuration
url = "http://127.0.0.1:8000/rank-resumes"
resume_folder = "./Resume"  # The path to your folder
target_keywords = "SQL, Engineer, Python"

# 2. Gather all files from the folder
files_to_send = []

# List all files in the directory
for filename in os.listdir(resume_folder):
    # Filter for supported file types
    if filename.lower().endswith(('.pdf', '.docx', '.jpg', '.jpeg', '.png')):
        file_path = os.path.join(resume_folder, filename)
        
        # Open the file in binary mode and add it to our list
        # Format: ('files', (filename, file_handle))
        files_to_send.append(
            ('files', (filename, open(file_path, 'rb')))
        )

if not files_to_send:
    print(f"No valid resumes found in {resume_folder}")
else:
    print(f"Sending {len(files_to_send)} resumes to the API...")

    # 3. Send everything in ONE request
    response = requests.post(
        url, 
        data={'skills': target_keywords}, 
        files=files_to_send
    )

    # 4. Handle the results
    if response.status_code == 200:
        data = response.json()
        print("\n--- RANKING RESULTS ---")
        for rank in data['rankings']:
            print(f"Score: {rank['score']} | File: {rank['filename']} | Matches: {rank['matched_skills']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    # 5. Clean up: Close all opened files
    for _, file_tuple in files_to_send:
        file_tuple[1].close()