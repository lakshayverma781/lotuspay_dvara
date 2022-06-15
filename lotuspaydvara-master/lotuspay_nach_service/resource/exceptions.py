from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class MyCustomException(Exception):
    def __init__(self, name: str):
        self.name = name


# @app.exception_handler(MyCustomException)
# async def MyCustomExceptionHandler(exception: MyCustomException):
#     return JSONResponse (status_code = 500, content = {"message": "Something critical happened"})