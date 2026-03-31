from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db
from typing import List

router = APIRouter(prefix="/api", tags=["issues"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/save/{issue_key}")
def save_issue(issue_key: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Check if already saved
    existing = db.query(models.SavedIssue).filter(
        models.SavedIssue.user_id == user.id,
        models.SavedIssue.issue_key == issue_key
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Issue already saved")

    saved = models.SavedIssue(issue_key=issue_key, user_id=user.id)
    db.add(saved)

    # Add to search history
    history = models.SearchHistory(issue_key=issue_key, user_id=user.id)
    db.add(history)

    db.commit()
    return {"message": f"Issue '{issue_key}' saved successfully"}

@router.get("/saved", response_model=List[schemas.SavedIssueOut])
def get_saved_issues(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.saved_issues

@router.delete("/saved/{issue_key}")
def delete_saved_issue(issue_key: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    saved = db.query(models.SavedIssue).filter(
        models.SavedIssue.user_id == user.id,
        models.SavedIssue.issue_key == issue_key
    ).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved issue not found")

    db.delete(saved)
    db.commit()
    return {"message": f"Issue '{issue_key}' removed from saved"}

@router.get("/history", response_model=List[schemas.SearchHistoryOut])
def get_history(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = auth.get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.search_history
