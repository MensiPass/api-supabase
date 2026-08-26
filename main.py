import os
from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI()
#check supabase connection
@app.on_event("startup")
def startup():
    try:
        supabase.auth.get_session()
        print("Server running on port 8000")
        print("Connected to Supabase")
    except Exception as e:
        print(f"Supabase connection failed: {e}")
        raise
    
@app.get("/")
def root():
    return {"message": "API is running"}