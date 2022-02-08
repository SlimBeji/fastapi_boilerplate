import uvicorn

from postman.app import create_app

app = create_app()


@app.get("/")
async def index():
    return {"message": "Hello World!", "name": "Slim Beji"}


if __name__ == "__main__":
    uvicorn.run(app)
