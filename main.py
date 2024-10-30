
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import organizations, hospitals, departments, providers, patients, users

app = FastAPI(title="Infoctor EHR API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
app.include_router(hospitals.router, prefix="/hospitals", tags=["hospitals"])
app.include_router(departments.router, prefix="/departments", tags=["departments"])
app.include_router(providers.router, prefix="/providers", tags=["providers"])
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(users.router, prefix="/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to Infoctor EHR API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
