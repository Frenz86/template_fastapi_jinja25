from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import ORJSONResponse
import uvicorn

from datetime import datetime
from database import get_db, engine, Base
from models import User
from schemas import UserCreate, UserResponse
from crud import create_user, get_users, get_user, update_user, delete_user

from fastapi.middleware.cors import CORSMiddleware

# Create database and tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
                default_response_class=ORJSONResponse,
                title="FastAPI CRUD App", 
                version="1.0.0",
                description="Un'applicazione CRUD completa con FastAPI, SQLite e Jinja2",
                docs_url="/api", #instead /docs
                redoc_url="/redoc"
                )

# Mount static files
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Initialize templates  
templates = Jinja2Templates(directory="../templates")

# CORS middleware for development
#from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["http://localhost:3000", "http://localhost:8000"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )

#######################################################################################
# # pip install scalar-fastapi
# from scalar_fastapi import get_scalar_api_reference

# # go to http://127.0.0.1:8000/scalar
# # from scalar_fastapi import get_scalar_api_reference

# @app.get("/scalar", include_in_schema=False)
# async def scalar_html():
#     return get_scalar_api_reference(
#                                     openapi_url=app.openapi_url,
#                                     title=app.title + " - Scalar",
#                                     )

#######################################################################################

# Add custom template functions
def format_datetime(dt):
    """Formatta datetime per i template"""
    if dt:
        return dt.strftime('%d/%m/%Y alle %H:%M')
    return 'N/A'

def format_date(dt):
    """Formatta solo la data per i template"""
    if dt:
        return dt.strftime('%d/%m/%Y')
    return 'N/A'

# Register template functions
templates.env.filters['datetime'] = format_datetime
templates.env.filters['date'] = format_date
templates.env.globals['now'] = datetime.now

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
            "status": "healthy",
            "service": "FastAPI CRUD App",
            "version": "1.0.0",
            }

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    try:
        users = get_users(db)
        success_message = request.query_params.get("success")
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "users": users,
            "title": "Gestione Utenti",
            "success": success_message,
            "current_time": datetime.now()
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "users": [],
            "title": "Gestione Utenti",
            "error": f"Errore nel caricamento: {str(e)}",
            "current_time": datetime.now()
        })

# Create user form
@app.get("/users/create", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {
        "request": request,
        "title": "Crea Nuovo Utente"
    })

# Handle user creation
@app.post("/users/create")
async def create_user_post(
                            request: Request,
                            name: str = Form(...),
                            email: str = Form(...),
                            age: int = Form(None),
                            db: Session = Depends(get_db)
                            ):
    try:
        # Validazione base
        if not name.strip():
            raise ValueError("Il nome non può essere vuoto")
        
        user_data = UserCreate(name=name.strip(), email=email.strip(), age=age)
        user = create_user(db, user_data)
        return RedirectResponse(url="/?success=Utente creato con successo", status_code=303)
    except ValueError as e:
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "title": "Crea Nuovo Utente",
            "error": str(e),
            "form_data": {"name": name, "email": email, "age": age}
        })
    except Exception as e:
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "title": "Crea Nuovo Utente",
            "error": f"Errore nella creazione: {str(e)}",
            "form_data": {"name": name, "email": email, "age": age}
        })

# Edit user form
@app.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_form(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
    return templates.TemplateResponse("edit_user.html", {
        "request": request,
        "user": user,
        "title": f"Modifica {user.name}"
    })

# Handle user update
@app.post("/users/{user_id}/edit")
async def update_user_post(
                            request: Request,
                            user_id: int,
                            name: str = Form(...),
                            email: str = Form(...),
                            age: int = Form(None),
                            db: Session = Depends(get_db)
                            ):
    try:
        # Validazione base
        if not name.strip():
            raise ValueError("Il nome non può essere vuoto")
            
        user_data = UserCreate(name=name.strip(), email=email.strip(), age=age)
        user = update_user(db, user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        return RedirectResponse(url="/?success=Utente aggiornato con successo", status_code=303)
    except ValueError as e:
        user = get_user(db, user_id)
        return templates.TemplateResponse("edit_user.html", {
            "request": request,
            "user": user,
            "title": f"Modifica {user.name if user else 'Utente'}",
            "error": str(e)
        })
    except Exception as e:
        user = get_user(db, user_id)
        return templates.TemplateResponse("edit_user.html", {
            "request": request,
            "user": user,
            "title": f"Modifica {user.name if user else 'Utente'}",
            "error": f"Errore nell'aggiornamento: {str(e)}"
        })

# Delete user
@app.post("/users/{user_id}/delete")
async def delete_user_post(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return RedirectResponse(url="/?success=Utente eliminato con successo", status_code=303)

# API Endpoints (JSON)
@app.get("/api/users", response_model=list[UserResponse], tags=["API"])
async def api_get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Ottiene la lista degli utenti con paginazione"""
    return get_users(db, skip=skip, limit=limit)

@app.post("/api/users", response_model=UserResponse, tags=["API"])
async def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crea un nuovo utente"""
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["API"])
async def api_get_user(user_id: int, db: Session = Depends(get_db)):
    """Ottiene un utente specifico per ID"""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user

@app.put("/api/users/{user_id}", response_model=UserResponse, tags=["API"])
async def api_update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """Aggiorna un utente esistente"""
    try:
        updated_user = update_user(db, user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/users/{user_id}", tags=["API"])
async def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    """Elimina un utente"""
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return {"message": "Utente eliminato con successo"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {
                                                    "request": request,
                                                    "title": "Pagina Non Trovata"
                                                    }, status_code=404
                                    )

#####################################################################################

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True,log_level="info")