from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from v1.routes import auth


app = FastAPI()


origins = []  # from v1.config.py


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.auth_router, tags=['Users'], prefix='/api/users')


@app.get("/api/healthcheck")
async def get_healthcheck():
    return {"API version": "1.0",
            "Status": "Running"}
