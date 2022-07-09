from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html = True), name="static")

@app.get("/print")
async def read_print_page():
    return FileResponse('static/print.html')

@app.get("/config")
async def read_print_page():
    return FileResponse('static/config.html')

@app.get("/change_fillament")
async def read_print_page():
    return FileResponse('static/change_fillament.html')

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
