import requests
import os
import time  # New: To track client-side time

# 1. Configuration
url = "http://127.0.0.1:8000/rank-resumes"
resume_folder = [
    "./INFORMATION-TECHNOLOGY",
    "./Resume"
    ]  
target_keywords = "Tenaga"

# 2. Gather all files from the folder
files_to_send = []

# List all files in the directory
for folder in resume_folder:
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.pdf', '.docx', '.jpg', '.jpeg', '.png')):
            file_path = os.path.join(folder, filename)
            files_to_send.append(
                ('files', (filename, open(file_path, 'rb')))
            )

if not files_to_send:
    print(f"No valid resumes found in {resume_folder}")
else:
    print(f"Sending {len(files_to_send)} resumes to the API...")

    # --- TIME TRACKING START ---
    start_time = time.time() 

    # 3. Send everything in ONE request
    try:
        response = requests.post(
            url, 
            data={'skills': target_keywords}, 
            files=files_to_send
        )
        
        end_time = time.time() 
        # --- TIME TRACKING END ---

        # 4. Handle the results
        if response.status_code == 200:
            data = response.json()
            total_roundtrip = round(end_time - start_time, 2)

            print("\n" + "="*95)
            print(f"{'FILENAME':<35} | {'SCORE':<5} | {'AI TIME (s)':<12} | {'MATCHED SKILLS'}")
            print("-" * 95)
            
            for rank in data['rankings']:
                # 'time_taken_sec' is the per-resume time from the server
                print(f"{rank['filename'][:35]:<35} | {rank['score']:<5} | {rank['time_taken_sec']:<12} | {', '.join(rank['matched_skills'])}")
            
            print("-" * 95)
            print(f"Total Server Processing Time: {data['total_processing_time_sec']} seconds")
            print(f"Total Round-Trip Time:      {total_roundtrip} seconds (includes file upload/download)")
            print("="*95)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # 5. Clean up: Close all opened files
    for _, file_tuple in files_to_send:
        file_tuple[1].close()