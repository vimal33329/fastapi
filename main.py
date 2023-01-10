from fastapi import FastAPI
from accountsummary.API import account

app = FastAPI()

app.include_router(account.router)

