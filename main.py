import uvicorn

from postman.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app)
