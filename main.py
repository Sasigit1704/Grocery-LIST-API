from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import items, lists

app = FastAPI(
    title="Grocery List API",
    description="""
This API manages grocery lists and items.

Features:
- Create grocery items
- Update items
- Delete items
- View grocery list
- Calculate total quantity

Built using FastAPI with proper validation and REST principles.
""",
    version="1.0.0"
)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(lists.router)