from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from database import init_db
from routes.tickets import router as tickets_router

app = FastAPI(title="Datastraw CRM", version="1.0.0")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    init_db()


app.include_router(tickets_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.get("/tickets/{ticket_id}", response_class=HTMLResponse)
def ticket_detail_page(request: Request, ticket_id: str):
    return templates.TemplateResponse("detail.html", {"request": request, "ticket_id": ticket_id})
