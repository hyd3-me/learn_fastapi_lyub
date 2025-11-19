from fastapi import FastAPI, Header

app = FastAPI()


@app.post("/hi")
def greet(who: str = Header()):
    return f"hi, {who}"


@app.get("/happy")
def happy(status_code=200):
    return ":)"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello:app", reload=True)
