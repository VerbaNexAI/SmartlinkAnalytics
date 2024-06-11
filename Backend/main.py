from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
