from fastapi.middleware.cors import CORSMiddleware


def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
       # allow_origins=[
        #   "http://localhost:5173",
        #   "http://uniattend-frontend:3000",
         #   "http://localhost:3000",
        #],
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
