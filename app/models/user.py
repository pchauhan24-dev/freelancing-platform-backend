from datetime import datetime, timezone


def create_user_document(
    name: str,
    email: str,
    password: str,
    role: str
):
    return {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "created_at": datetime.now(timezone.utc)
    }