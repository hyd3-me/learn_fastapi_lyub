from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from web import explorer, creature, user
from fastapi import File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
from typing import Generator


app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

# Каталог, содержащий файл main.py:
top = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=f"{top}/static", html=True), name="free")


@app.get("/")
def top():
    return "top here"


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"


@app.get("/who2")
def greet2(name: str = Form()):
    return f"Hello, {name}?"


@app.post("/small")
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"file size: {len(small_file)}"


@app.post("/big")
async def upload_big_file(big_file: UploadFile) -> str:
    return f"file size: {big_file.size}, name: {big_file.filename}"


@app.get("/small/{name}")
async def download_small_file(name):
    return FileResponse(name)


def gen_file(path: str) -> Generator:
    with open(file=path, mode="rb") as file:
        yield file.read()


@app.get("/big/{name}")
async def download_big_file(name: str):
    gen_expr = gen_file(path=name)
    response = StreamingResponse(
        content=gen_expr,
        status_code=200,
    )
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
