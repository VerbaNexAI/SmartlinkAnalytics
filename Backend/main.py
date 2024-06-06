from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.router import router

app = FastAPI()



# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(router)



# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
