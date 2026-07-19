from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.database import engine, Base
from app.routes.auth.auth import router as auth_router
from app.routes.events.event import router as event_router
from app.routes.registration.registration import router as registration_router
from app.middleware import add_cors 

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the app starts: safely create tables
    try:
        #Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
    yield
    # This runs when the app shuts down (for cleanup if needed)

# Initialize the app with the lifespan
app = FastAPI(lifespan=lifespan)

# Add Middleware and Routes
add_cors(app)
security = HTTPBearer()

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(registration_router)

@app.get("/routes")
def get_routes():
    return [{"path": route.path, "name": route.name} for route in app.routes]

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

