from fastapi import FastAPI, Depends, Params

app = FastAPI()


# функция зависимости:
def user_dep(name: str = Params, password: str = Params):
    return {"name": name, "valid": True}


# функция пути/конечная точка веб-приложения:
@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user
