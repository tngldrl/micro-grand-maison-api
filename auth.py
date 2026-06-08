from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
import models

# Note: In a production environment with a working SSL module, 
# we would use `firebase_admin.auth.verify_id_token` here.
# Due to the local environment's SSL restrictions, this is a mock implementation
# that accepts the frontend token as the user ID for demo purposes.

def verify_token(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
        
    token = authorization.split("Bearer ")[1]
    
    if token == "guest":
        # Guest mode
        return {"uid": "guest", "is_anonymous": True}
        
    # Mock token verification (using token directly as uid for demo)
    uid = token[:30] # Just truncate for a dummy ID
    
    # Check if user exists in DB
    user = db.query(models.User).filter(models.User.id == uid).first()
    if not user:
        # Auto-register user
        user = models.User(id=uid, email=f"{uid}@example.com", display_name="GitHub User")
        db.add(user)
        db.commit()
        db.refresh(user)
        
    return {"uid": user.id, "email": user.email, "is_anonymous": False}
