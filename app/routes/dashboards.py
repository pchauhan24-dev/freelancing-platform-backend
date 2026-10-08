from fastapi import APIRouter, Depends

from app.database import projects_collection, proposals_collection
from app.utils.dependencies import require_client, require_freelancer

router = APIRouter(prefix="/dashboard", tags=["Dashboards"])


@router.get("/client")
def client_dashboard(current_user=Depends(require_client)):
    client_id = current_user["user_id"]

    total_projects = projects_collection.count_documents({
        "client_id": client_id
    })

    active_projects = projects_collection.count_documents({
        "client_id": client_id,
        "status": "In Progress"
    })

    completed_projects = projects_collection.count_documents({
        "client_id": client_id,
        "status": "Completed"
    })

    client_projects = projects_collection.find(
        {"client_id": client_id},
        {"_id": 1}
    )

    project_ids = [str(project["_id"]) for project in client_projects]

    total_proposals = proposals_collection.count_documents({
        "project_id": {"$in": project_ids}
    })

    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed_projects": completed_projects,
        "total_proposals_received": total_proposals
    }


@router.get("/freelancer")
def freelancer_dashboard(current_user=Depends(require_freelancer)):
    freelancer_id = current_user["user_id"]

    applied_projects = proposals_collection.count_documents({
        "freelancer_id": freelancer_id
    })

    accepted_proposals = proposals_collection.count_documents({
        "freelancer_id": freelancer_id,
        "status": "Accepted"
    })

    accepted = proposals_collection.find(
        {
            "freelancer_id": freelancer_id,
            "status": "Accepted"
        },
        {"project_id": 1}
    )

    accepted_project_ids = [project["project_id"] for project in accepted]

    active_projects = projects_collection.count_documents({
        "_id": {
            "$in": [
                __import__("bson").ObjectId(project_id)
                for project_id in accepted_project_ids
                if __import__("bson").ObjectId.is_valid(project_id)
            ]
        },
        "status": "In Progress"
    })

    completed_projects = projects_collection.count_documents({
        "_id": {
            "$in": [
                __import__("bson").ObjectId(project_id)
                for project_id in accepted_project_ids
                if __import__("bson").ObjectId.is_valid(project_id)
            ]
        },
        "status": "Completed"
    })

    return {
        "applied_projects": applied_projects,
        "active_projects": active_projects,
        "completed_projects": completed_projects,
        "accepted_proposals": accepted_proposals
    }