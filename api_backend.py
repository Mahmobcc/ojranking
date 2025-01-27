from fastapi import FastAPI
import requests
import time
import threading

app = FastAPI()

# Cache to store user solve counts
cache = {}

def fetch_data():
    # List of user IDs
    uhunt_ids = [123456, 654321]  # Replace with actual uHunt IDs
    codeforces_ids = ["user1", "user2"]  # Replace with actual Codeforces handles
    
    # Fetch uHunt data
    for user_id in uhunt_ids:
        response = requests.get(f"https://uhunt.onlinejudge.org/api/user/{user_id}")
        if response.status_code == 200:
            cache[user_id] = {"uhunt": response.json()["solved"]}
    
    # Fetch Codeforces data
    for handle in codeforces_ids:
        response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}")
        if response.status_code == 200:
            solved_count = len(set([problem["contestId"] for problem in response.json()["result"] if problem["verdict"] == "OK"]))
            cache[handle] = {"codeforces": solved_count}

# Run fetch_data every 2 hours
def update_data():
    while True:
        fetch_data()
        time.sleep(7200)  # 2 hours

thread = threading.Thread(target=update_data, daemon=True)
thread.start()

@app.get("/solve-counts")
def get_solve_counts():
    return cache
