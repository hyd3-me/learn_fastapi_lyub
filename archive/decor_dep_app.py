from fastapi import FastAPI, Depends, Params

app = FastAPI()


# функция зависимости:
def check_dep(name: str = Params, password: str = Params):
    if not name:
        raise


# функция пути/конечная точка веб-приложения:
@app.get("/check_user", dependencies=[Depends(check_dep)])
def check_user() -> bool:
    return True
