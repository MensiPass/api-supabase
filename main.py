import os
from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

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

#sign up body model
class SignupReq(BaseModel):
    email: str | None = None
    password: str | None = None
class LoginRequest(BaseModel):
    email: str | None = None
    password: str | None = None
#--------------------------------------
#Stage 0 ----------------
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

#Stage 1 ---------------------------
#sign up call
@app.post("/auth/signup",description="Created", status_code=201)
def sign_up(req: SignupReq):
    if not req.email or not req.password:
         raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )
    try:
        res = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password
        })

        return res.user

    except Exception as e:
        print(f"Supabase signup error: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
#log in call
@app.post("/auth/login",description="Logged in", status_code=200)
def sign_up(req: LoginRequest):
    if not req.email or not req.password:
         raise HTTPException(
            status_code=400,
            content={"error": "Email and password are required"}
        )
    try:
        res = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })

        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token
        }

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"}
        )