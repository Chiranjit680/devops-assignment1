from fastapi import FastAPI
from .database import engine, SessionLocal
from .models import Base, User

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "fastapi + postgres running"}
@app.get("/users/")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users    
@app.post("/users/{name}")
def create_user(name: str):
    db = SessionLocal()
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"id": user.id, "name": user.name}
