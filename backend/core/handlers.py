from fastapi.responses import JSONResponse
from fastapi import Request, app

from backend.core.exceptions import AppException

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
 return JSONResponse(
    status_code=exc.status_code,
    content={
        "error_code": exc.error_code,
        "message": exc.message
    }
 )