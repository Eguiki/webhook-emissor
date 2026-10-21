from urllib import request

import httpx
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request,"send_item.html", {"request": request})

@app.post("/")
async def send_item(request: Request):
    form = await request.form()

    item = {
        "title": form["title"],
        "quantity": form["quantity"],
        "price": form["price"]
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            "http://127.0.0.1:8000/webhook/new-item",
            json=item
        )

    return {
        "message": "Webhook enviado!",
        "response": response.json()
    }