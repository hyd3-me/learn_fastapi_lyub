from fastapi import FastAPI
from web import explorer, creature, user
from fastapi import File


app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


@app.get("/")
def top():
    return "top here"


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"


@app.post("/small")
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"file size: {len(small_file)}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
