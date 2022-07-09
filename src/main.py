import glob

from typing import Union

from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="static")

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}

@app.get("/print", response_class=HTMLResponse)
async def read_print_page(request: Request):
    file_list = list(glob.glob("~/3d_models/*.gcode"))
    print(file_list)
    return templates.TemplateResponse("print.html", {"request": request, "files": file_list})

@app.get("/config", response_class=HTMLResponse)
async def read_config_page(request: Request):
    return templates.TemplateResponse("config.html", {"request": request})

@app.get("/change_fillament", response_class=HTMLResponse)
async def read_change_fillament_page(request: Request):
    return templates.TemplateResponse("change_fillament.html", {"request": request})

app.mount("/", StaticFiles(directory="static", html = True), name="static")
