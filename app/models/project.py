from datetime import datetime, timezone


def create_project_document(
    client_id: str,
    title: str,
    category: str,
    budget: float,
    description: str,
    required_skills: list[str],
    deadline: datetime,
    experience_level: str
):
    return {
        "client_id": client_id,
        "title": title,
        "category": category,
        "budget": budget,
        "description": description,
        "required_skills": required_skills,
        "deadline": deadline,
        "experience_level": experience_level,
        "status": "Open",
        "created_at": datetime.now(timezone.utc)
    }