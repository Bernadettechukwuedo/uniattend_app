from fastapi import FastAPI
from app.database import SessionLocal, engine,Base
from  app.routes.auth.auth import router as auth_router
from app.routes.events.event import router as event_router
from app.routes.registration.registration import router as registration_router
from app.models import User
from fastapi.security import HTTPBearer
from app.middleware import add_cors 
from fastapi.staticfiles import StaticFiles



app = FastAPI()
add_cors(app)
Base.metadata.create_all(bind=engine)

security= HTTPBearer()
app.include_router(auth_router)
app.include_router(event_router)
app.include_router(registration_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
