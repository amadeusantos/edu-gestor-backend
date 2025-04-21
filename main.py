from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.auth.routers import router as auth_router
from api.user.routers import router as user_router
from api.professor.routers import router as professor_router
from api.student.routers import router as student_router
from api.classroom.routers import router as classroom_router
from api.discipline.routers import router as discipline_router
from api.frequency.routers import router as frequency_router
from api.exceptions import ServiceException

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.exception_handler(ServiceException)
async def service_exception_handler(_, exc: ServiceException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message, "error_code": exc.error_code})


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(professor_router)
app.include_router(student_router)
app.include_router(classroom_router)
app.include_router(discipline_router)
app.include_router(frequency_router)
