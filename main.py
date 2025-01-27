from fastapi import FastAPI
import requests
import time
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mahmobcc.github.io/"],  # Allow all origins, but you can limit this for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Cache to store user solve counts
cache = {}

def fetch_data():
    # List of user IDs
    uhunt_ids = ["mahmodul00", 654321]  # Replace with actual uHunt IDs
    codeforces_ids = ["mahmodul00", "user2"]  # Replace with actual Codeforces handles
    
    # Fetch uHunt data
    for user_id in uhunt_ids:
        response = requests.get(f"https://uhunt.onlinejudge.org/u/{user_id}")
        if response.status_code == 200:
            cache[user_id] = {"uhunt": response.json()["solved"]}
        else:
            print("Not Found uHunt")
    
    # Fetch Codeforces data
    for handle in codeforces_ids:
        response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}")
        if response.status_code == 200:
            #solved_count = len(set([problem["contestId"] for problem in response.json()["result"] if problem["verdict"] == "OK"]))
            cache[handle] = {"codeforces": response.json()["newRating"]}
        else:
            print("Not Found CodeForces")

# Run fetch_data every 2 hours
def update_data():
    while True:
        fetch_data()
        time.sleep(7200)  # 2 hours

thread = threading.Thread(target=update_data, daemon=True)
thread.start()

@app.get("/solve-counts")
def get_solve_counts():
    if not cache:
        return {"message": "Cache is empty, no solve counts available."}
    return cache
