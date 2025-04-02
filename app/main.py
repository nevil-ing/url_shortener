from fastapi import FastAPI, HTTPException

app = FastAPI( title = "A FastAPI url Shortener")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)
