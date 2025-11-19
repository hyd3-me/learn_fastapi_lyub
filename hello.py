from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def greet(who):
    return f"hi, {who}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello:app", reload=True)
