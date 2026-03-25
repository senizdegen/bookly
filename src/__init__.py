from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import (
    UserAlreadyExists,
    create_exception_handler
)

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message":"User with email already exists",
            "error_code":"user_exists"
        }
    )
)

#add others exceptions

@app.exception_handler(500)
async def internal_server_error(request, exc):
    return JSONResponse(
        content={
            "message":"Oops! Something went wrong",
            "error_code":"server_error"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])
