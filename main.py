from fastapi import FastAPI
from routers import items, lists

app = FastAPI()

app.include_router(items.router)
app.include_router(lists.router)