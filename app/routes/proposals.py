from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import projects_collection, proposals_collection
from app.models.proposal import create_proposal_document
from app.schemas.proposal import ProposalCreate
from app.utils.dependencies import require_client, require_freelancer


router = APIRouter(prefix="/projects", tags=["Proposals"])


@router.get("/my-proposals")
def get_my_proposals(current_user=Depends(require_freelancer)):
    proposals = list(
        proposals_collection.find({
            "freelancer_id": current_user["user_id"]
        })
    )

    for proposal in proposals:
        proposal["_id"] = str(proposal["_id"])

    return {
        "count": len(proposals),
        "proposals": proposals
    }

@router.get("/{project_id}/proposals")
def get_project_proposals(
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
            detail="You can only view proposals for your own projects"
        )

    proposals = list(
        proposals_collection.find({
            "project_id": project_id
        })
    )

    for proposal in proposals:
        proposal["_id"] = str(proposal["_id"])

    return {
        "project_id": project_id,
        "count": len(proposals),
        "proposals": proposals
    }

@router.post("/{project_id}/proposal")
def submit_proposal(
    project_id: str,
    proposal: ProposalCreate,
    current_user=Depends(require_freelancer)
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

    if project["status"] != "Open":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Proposals can only be submitted for open projects"
        )

    existing_proposal = proposals_collection.find_one({
        "project_id": project_id,
        "freelancer_id": current_user["user_id"]
    })

    if existing_proposal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted a proposal for this project"
        )

    proposal_document = create_proposal_document(
        project_id=project_id,
        freelancer_id=current_user["user_id"],
        bid_amount=proposal.bid_amount,
        cover_letter=proposal.cover_letter,
        delivery_time=proposal.delivery_time
    )

    result = proposals_collection.insert_one(proposal_document)

    return {
        "message": "Proposal submitted successfully",
        "proposal_id": str(result.inserted_id)
    }

@router.put("/proposal/{proposal_id}/accept")
def accept_proposal(
    proposal_id: str,
    current_user=Depends(require_client)
):
    if not ObjectId.is_valid(proposal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid proposal ID"
        )

    proposal = proposals_collection.find_one({
        "_id": ObjectId(proposal_id)
    })

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )

    project = projects_collection.find_one({
        "_id": ObjectId(proposal["project_id"])
    })

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage proposals for your own projects"
        )

    if proposal["status"] != "Pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending proposals can be accepted"
        )

    proposals_collection.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": "Accepted"}}
    )

    return {
        "message": "Proposal accepted successfully",
        "proposal_id": proposal_id
    }


@router.put("/proposal/{proposal_id}/reject")
def reject_proposal(
    proposal_id: str,
    current_user=Depends(require_client)
):
    if not ObjectId.is_valid(proposal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid proposal ID"
        )

    proposal = proposals_collection.find_one({
        "_id": ObjectId(proposal_id)
    })

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )

    project = projects_collection.find_one({
        "_id": ObjectId(proposal["project_id"])
    })

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage proposals for your own projects"
        )

    if proposal["status"] != "Pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending proposals can be rejected"
        )

    proposals_collection.update_one(
        {"_id": ObjectId(proposal_id)},
        {"$set": {"status": "Rejected"}}
    )

    return {
        "message": "Proposal rejected successfully",
        "proposal_id": proposal_id
    }

@router.delete("/proposal/{proposal_id}")
def withdraw_proposal(
    proposal_id: str,
    current_user=Depends(require_freelancer)
):
    if not ObjectId.is_valid(proposal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid proposal ID"
        )

    proposal = proposals_collection.find_one({
        "_id": ObjectId(proposal_id)
    })

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )

    if proposal["freelancer_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only withdraw your own proposals"
        )

    if proposal["status"] != "Pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending proposals can be withdrawn"
        )

    proposals_collection.delete_one({
        "_id": ObjectId(proposal_id)
    })

    return {
        "message": "Proposal withdrawn successfully",
        "proposal_id": proposal_id
    }