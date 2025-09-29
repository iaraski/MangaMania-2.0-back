from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .user import router as user_router
from .composition import router as composition_router
from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.encoders import jsonable_encoder

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/api")
app.include_router(composition_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Backend работает!"}



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
