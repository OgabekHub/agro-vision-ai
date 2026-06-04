"""User authentication endpoints using Supabase Auth."""

import logging
import re
from typing import Optional
from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel
from app.core.supabase_service import get_supabase

logger = logging.getLogger(__name__)
router = APIRouter()

# Simple email regex validation helper
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(req: RegisterRequest):
    """Register a new user using Supabase Auth and save profile to public users table."""
    email = req.email.strip().lower()
    full_name = req.full_name.strip()
    password = req.password

    # Validate email
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Noto'g'ri elektron pochta formati",
        )

    # Validate password length
    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parol kamida 6 ta belgidan iborat bo'lishi kerak",
        )

    client = get_supabase()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ma'lumotlar bazasi bilan aloqa yo'q",
        )

    try:
        # 1. Sign up user in Supabase Auth
        res = client.auth.sign_up({"email": email, "password": password})
        if not res.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ro'yxatdan o'tish amalga oshmadi",
            )

        user_id = res.user.id

        # 2. Assign role: 'admin' if email is olimjonov.ogabek.dev@gmail.com, else 'user'
        role = "admin" if email == "olimjonov.ogabek.dev@gmail.com" else "user"

        # 3. Create profile in public users table using clean service_role client
        profile = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "role": role,
        }
        db_client = get_supabase()
        if not db_client:
            raise Exception("Ma'lumotlar bazasi bilan bog'lanib bo'lmadi")
        db_client.table("users").insert(profile).execute()

        logger.info(f"✅ Yangi foydalanuvchi ro'yxatdan o'tdi: {email} (Rol: {role})")
        return {
            "success": True,
            "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
            "data": {
                "id": user_id,
                "email": email,
                "full_name": full_name,
                "role": role,
            },
        }
    except Exception as e:
        logger.error(f"Ro'yxatdan o'tishda xato: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login")
async def login(req: LoginRequest):
    """Log in user using Supabase Auth and return JWT access token."""
    email = req.email.strip().lower()
    password = req.password

    client = get_supabase()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ma'lumotlar bazasi bilan aloqa yo'q",
        )

    try:
        # Sign in with password
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        if not res.session or not res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Elektron pochta yoki parol xato",
            )

        # Get profile from public users table to retrieve role using clean service_role client
        db_client = get_supabase()
        if not db_client:
            raise Exception("Ma'lumotlar bazasi bilan bog'lanib bo'lmadi")
            
        user_profile = db_client.table("users").select("*").eq("id", res.user.id).execute().data
        role = "user"
        full_name = "Foydalanuvchi"

        if user_profile:
            role = user_profile[0].get("role", "user")
            full_name = user_profile[0].get("full_name", "Foydalanuvchi")
        else:
            # Fallback in case table insert failed during register: create it now
            role = "admin" if email == "olimjonov.ogabek.dev@gmail.com" else "user"
            profile = {
                "id": res.user.id,
                "email": email,
                "full_name": full_name,
                "role": role,
            }
            db_client.table("users").insert(profile).execute()

        logger.info(f"🔑 Foydalanuvchi tizimga kirdi: {email} (Rol: {role})")
        return {
            "success": True,
            "data": {
                "access_token": res.session.access_token,
                "token_type": "bearer",
                "user": {
                    "id": res.user.id,
                    "email": email,
                    "full_name": full_name,
                    "role": role,
                },
            },
        }
    except Exception as e:
        logger.error(f"Tizimga kirishda xato: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Elektron pochta yoki parol xato",
        )


@router.get("/me")
async def get_me(authorization: Optional[str] = Header(None)):
    """Get authenticated user profile."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token topilmadi yoki noto'g'ri",
        )

    token = authorization.split(" ")[1]
    client = get_supabase()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ma'lumotlar bazasi bilan aloqa yo'q",
        )

    try:
        user_res = client.auth.get_user(token)
        if not user_res or not user_res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Yaroqsiz token",
            )

        user_profile = client.table("users").select("*").eq("id", user_res.user.id).execute().data
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Foydalanuvchi profili topilmadi",
            )

        return {
            "success": True,
            "data": {
                "id": user_profile[0]["id"],
                "email": user_profile[0]["email"],
                "full_name": user_profile[0]["full_name"],
                "role": user_profile[0]["role"],
            },
        }
    except Exception as e:
        logger.error(f"Token tekshirishda xato: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token muddati o'tgan yoki yaroqsiz",
        )
