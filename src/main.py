from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()
# app.mount("/", StaticFiles(directory="static", html = True), name="static")

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
	<form action="/files/" enctype="multipart/form-data" method="post">
		<input name="files" type="file" multiple>
		<input type="submit">
	</form>
	<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
		<input name="files" type="file" multiple>
		<input type="submit">
	</form>
</body>
    """
    return HTMLResponse(content=content)
