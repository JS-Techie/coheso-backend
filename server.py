from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import setup_routes

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods= ['*'],
    allow_headers= ['*']
)


setup_routes(app)


@app.get("/")
async def root():
    return{'RESPONSE':'This is a coheso assignment'}
