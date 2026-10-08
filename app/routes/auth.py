from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database import users_collection
from app.models.user import create_user_document
from app.schemas.auth import UserLogin, UserSignup
from app.utils.auth import (
    create_access_token,
    hash_password,
    verify_password
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(user: UserSignup):

    # Check valid role
    if user.role not in ["Client", "Freelancer"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be Client or Freelancer"
        )

    # Check if email already exists
    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user document
    user_document = create_user_document(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    # Save user
    result = users_collection.insert_one(user_document)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "role": user.role
    }


@router.post("/login")
def login(user: UserLogin):

    # Find user
    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        user.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        str(existing_user["_id"]),
        existing_user["role"]
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "role": existing_user["role"]
    }