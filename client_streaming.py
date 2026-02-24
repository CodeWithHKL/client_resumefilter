import requests
import os
import time
import json

# 1. Configuration
url = "http://127.0.0.1:8000/rank-resumes"
resume_folders = [
    "./INFORMATION-TECHNOLOGY",
    "./Resume"
]
target_keywords = "python, sql, javascript, uniten"

# 2. Gather all files
files_to_send = []
for folder in resume_folders:
    if not os.path.exists(folder):
        continue
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.pdf', '.docx', '.jpg', '.jpeg', '.png')):
            file_path = os.path.join(folder, filename)
            files_to_send.append(
                ('files', (filename, open(file_path, 'rb')))
            )

if not files_to_send:
    print(f"No valid resumes found in {resume_folders}")
else:
    print(f"🚀 Started streaming {len(files_to_send)} resumes...")
    print("="*95)
    print(f"{'FILENAME':<35} | {'SCORE':<5} | {'TIME (s)':<12} | {'MATCHED SKILLS'}")
    print("-" * 95)
    
    start_time = time.time()
    all_results = []

    try:
        # 3. Stream=True allows us to process the response line-by-line
        with requests.post(url, data={'skills': target_keywords}, files=files_to_send, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        # Decode the JSON chunk
                        result = json.loads(line.decode('utf-8'))
                        all_results.append(result)

                        # Print the result immediately (No flickering)
                        skills_str = ", ".join(result.get('matched_skills', []))
                        print(f"{result['filename'][:35]:<35} | {result['score']:<5} | {result['time_taken_sec']:<12} | {skills_str}")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        # 4. Final Summary and Ranking
        end_time = time.time()
        total_roundtrip = round(end_time - start_time, 2)
        
        print("-" * 95)
        print(f"✅ Processing Complete! {len(all_results)} resumes in {total_roundtrip}s")
        print("-" * 95)

        # Show the Top 10 Ranking
        print("\n🏆 TOP 10 RANKING:")
        print(f"{'RANK':<5} | {'SCORE':<5} | {'FILENAME'}")
        print("-" * 45)
        
        all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
        for i, rank in enumerate(all_results[:10], 1):
            print(f"{i:<5} | {rank['score']:<5} | {rank['filename']}")
        print("="*95)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 5. Clean up
        for _, file_tuple in files_to_send:
            file_tuple[1].close()