from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.proposals import router as proposals_router
from app.routes.projects import router as projects_router
from app.routes.dashboards import router as dashboard_router

app = FastAPI(
    title="Freelancing Platform Backend API",
    description="Backend API for a Freelancing Marketplace",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(proposals_router)
app.include_router(projects_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "Freelancing Platform Backend API is running"}