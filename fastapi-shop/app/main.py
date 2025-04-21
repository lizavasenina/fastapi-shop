from fastapi import FastAPI

app = FastAPI(
    title="Интернет-магазин",
    description="Простейшая система управления онлайн-заказами "
    "зарегистрированных пользователей в интернет-магазине, "
    "основанная на фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Васенина Елизавета Андреевна",
        "email": "vasenina.ea@phystech.edu",
    }
)