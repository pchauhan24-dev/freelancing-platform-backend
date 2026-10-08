from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import projects_collection
from app.models.project import create_project_document
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.utils.dependencies import (
    get_current_user,
    require_client
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/")
def create_project(
    project: ProjectCreate,
    current_user=Depends(require_client)
):
    project_document = create_project_document(
        client_id=current_user["user_id"],
        title=project.title,
        category=project.category,
        budget=project.budget,
        description=project.description,
        required_skills=project.required_skills,
        deadline=project.deadline,
        experience_level=project.experience_level
    )

    result = projects_collection.insert_one(project_document)

    return {
        "message": "Project created successfully",
        "project_id": str(result.inserted_id)
    }


@router.get("/")
def get_projects(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None)
):
    query = {}

    if search:
        query["$or"] = [
        {"title": {"$regex": search, "$options": "i"}},
        {"description": {"$regex": search, "$options": "i"}},
        {"category": {"$regex": search, "$options": "i"}},
        {"required_skills": {"$regex": search, "$options": "i"}}
    ]

    if category:
        query["category"] = {
            "$regex": category,
            "$options": "i"
        }

    projects = list(
        projects_collection.find(query)
    )

    for project in projects:
        project["_id"] = str(project["_id"])
        project["client_id"] = str(project["client_id"])

    return {
        "count": len(projects),
        "projects": projects
    }


@router.get("/{project_id}")
def get_project(project_id: str):

    if not ObjectId.is_valid(project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project ID"
        )

    project = projects_collection.find_one(
        {"_id": ObjectId(project_id)}
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    project["_id"] = str(project["_id"])
    project["client_id"] = str(project["client_id"])

    return project


@router.put("/{project_id}/start")
def start_project(
    project_id: str,
    current_user=Depends(require_client)
):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project ID"
        )

    project = projects_collection.find_one({
        "_id": ObjectId(project_id)
    })

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own projects"
        )

    if project["status"] != "Open":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only open projects can be started"
        )

    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {"status": "In Progress"}}
    )

    return {
        "message": "Project started successfully",
        "project_id": project_id,
        "status": "In Progress"
    }


@router.put("/{project_id}/complete")
def complete_project(
    project_id: str,
    current_user=Depends(require_client)
):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project ID"
        )

    project = projects_collection.find_one({
        "_id": ObjectId(project_id)
    })

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own projects"
        )

    if project["status"] != "In Progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only projects in progress can be completed"
        )

    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {"status": "Completed"}}
    )

    return {
        "message": "Project completed successfully",
        "project_id": project_id,
        "status": "Completed"
    }


@router.put("/{project_id}/cancel")
def cancel_project(
    project_id: str,
    current_user=Depends(require_client)
):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project ID"
        )

    project = projects_collection.find_one({
        "_id": ObjectId(project_id)
    })

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own projects"
        )

    if project["status"] not in ["Open", "In Progress"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only open or in-progress projects can be cancelled"
        )

    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {"status": "Cancelled"}}
    )

    return {
        "message": "Project cancelled successfully",
        "project_id": project_id,
        "status": "Cancelled"
    }

@router.put("/{project_id}")
def update_project(
    project_id: str,
    project: ProjectUpdate,
    current_user=Depends(require_client)
):

    if not ObjectId.is_valid(project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project ID"
        )

    existing_project = projects_collection.find_one({
        "_id": ObjectId(project_id)
    })

    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if existing_project["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own projects"
        )

    update_data = project.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": update_data}
    )

    return {
        "message": "Project updated successfully"
    }


@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    current_user=Depends(require_client)
):

    if not ObjectId.is_valid(project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project ID"
        )

    existing_project = projects_collection.find_one({
        "_id": ObjectId(project_id)
    })

    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if existing_project["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own projects"
        )

    projects_collection.delete_one({
        "_id": ObjectId(project_id)
    })

    return {
        "message": "Project deleted successfully"
    }