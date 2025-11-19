from fastapi import FastAPI, Header, Response

app = FastAPI()


@app.post("/hi")
def greet(who: str = Header()):
    return f"hi, {who}"


@app.get("/happy")
def happy(status_code=200):
    return ":)"


@app.get("/set_header/{name}/{value}")
def set_header(name: str, value: str, response: Response):
    response.headers[name] = value
    return "normal body"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello:app", reload=True)
