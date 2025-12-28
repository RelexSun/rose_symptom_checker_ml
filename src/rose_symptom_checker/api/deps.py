from fastapi import Depends
from sqlalchemy.orm import Session
from rose_symptom_checker.db.session import get_db
from rose_symptom_checker.services.auth import get_current_user
from rose_symptom_checker.db.models.user import User

# Reusable dependencies
CurrentUser = Depends(get_current_user)
DatabaseSession = Depends(get_db)