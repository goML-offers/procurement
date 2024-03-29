from fastapi import FastAPI
import uvicorn
import os
import sys
sys.path.insert(0, 'LLM Procurement\\api\\')
from router import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# app.include_router(BusinessQueryRouter.router)
# app.include_router(userQueryRouter.router)
# app.include_router(organisationRouter.router)
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(router.router,tags=["Procurement"])
def run_server():

    uvicorn.run("app:app", host="127.0.0.1", port=8002, reload=True)
if __name__ == "__main__":
     print("test")
     run_server()