import os
import glob

from starlette.responses import FileResponse
import starlette.status as status

from typing import Union

from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="static")

app = FastAPI()

gcode_files_path = "/home/pi/3d_models/"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    # TODO: ne legyen internal server error akkor, amikor nincs file kiválasztva
    for f in files:
        with open(f"{gcode_files_path}{f.filename}", 'wb') as out_file:
            content = f.file.read()
            out_file.write(content)
    
    return RedirectResponse('/print',  status_code=status.HTTP_302_FOUND)

@app.get("/print", response_class=HTMLResponse)
async def read_print_page(request: Request):
    file_list = glob.glob(f"{gcode_files_path}*.gcode")
    file_list = [os.path.basename(fn) for fn in file_list]
    return templates.TemplateResponse("print.html", {"request": request, "files": file_list})

@app.get("/config", response_class=HTMLResponse)
async def read_config_page(request: Request):
    return templates.TemplateResponse("config.html", {"request": request})

@app.get("/change_fillament", response_class=HTMLResponse)
async def read_change_fillament_page(request: Request):
    return templates.TemplateResponse("change_fillament.html", {"request": request})

app.mount("/", StaticFiles(directory="static", html = True), name="static")
