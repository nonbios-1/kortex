from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

# Import from local modules with absolute imports
from database.config import SessionLocal
from database.models import PromptWorkflow as DBPromptWorkflow

app = FastAPI(
    title="Kortex API",
    description="API for Kortex prompt evaluation system",
    version="0.1.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class PromptWorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt_template: str
    parameters: Optional[dict] = None

class PromptWorkflowCreate(PromptWorkflowBase):
    pass

class PromptWorkflow(PromptWorkflowBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "name": "Kortex API",
        "version": "0.1.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "components": {
            "api": "ok",
            "database": "connected"
        }
    }

# CRUD endpoints for PromptWorkflow
@app.post("/workflows/", response_model=PromptWorkflow)
def create_workflow(workflow: PromptWorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = DBPromptWorkflow(
        name=workflow.name,
        description=workflow.description,
        prompt_template=workflow.prompt_template,
        parameters=workflow.parameters
    )
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@app.get("/workflows/", response_model=List[PromptWorkflow])
def list_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workflows = db.query(DBPromptWorkflow).offset(skip).limit(limit).all()
    return workflows

@app.get("/workflows/{workflow_id}", response_model=PromptWorkflow)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(DBPromptWorkflow).filter(DBPromptWorkflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@app.put("/workflows/{workflow_id}", response_model=PromptWorkflow)
def update_workflow(workflow_id: int, workflow: PromptWorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = db.query(DBPromptWorkflow).filter(DBPromptWorkflow.id == workflow_id).first()
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    for key, value in workflow.dict().items():
        setattr(db_workflow, key, value)
    
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@app.delete("/workflows/{workflow_id}")
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(DBPromptWorkflow).filter(DBPromptWorkflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    db.delete(workflow)
    db.commit()
    return {"message": "Workflow deleted successfully"}
