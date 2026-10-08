from datetime import datetime, timezone


def create_proposal_document(
    project_id: str,
    freelancer_id: str,
    bid_amount: float,
    cover_letter: str,
    delivery_time: int
):
    return {
        "project_id": project_id,
        "freelancer_id": freelancer_id,
        "bid_amount": bid_amount,
        "cover_letter": cover_letter,
        "delivery_time": delivery_time,
        "status": "Pending",
        "submitted_at": datetime.now(timezone.utc)
    }