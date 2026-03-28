from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import models, schemas
from database import engine, SessionLocal

# -------------------
# CONFIGURATION JWT
# -------------------
SECRET_KEY = "SECRET_KEY_SUPER_SECRET"  # change en prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------
# FASTAPI ET DB
# -------------------
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# FONCTIONS UTILITAIRES
# -------------------
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Token invalide")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# -------------------
# INSCRIPTION ET LOGIN
# -------------------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "message": "Utilisateur créé"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

# -------------------
# BUS
# -------------------
@app.post("/bus")
def add_bus(bus: schemas.BusCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    new_bus = models.Bus(**bus.dict())
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus

@app.get("/bus")
def get_all_bus(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Bus).all()

@app.put("/bus/{bus_id}")
def update_bus(bus_id: int, bus: schemas.BusUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Bus non trouvé")
    obj.numero = bus.numero
    obj.capacite = bus.capacite
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/bus/{bus_id}")
def delete_bus(bus_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Bus non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Bus supprimé"}

# -------------------
# CHAUFFEUR
# -------------------
@app.post("/chauffeur")
def add_chauffeur(ch: schemas.ChauffeurCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = models.Chauffeur(**ch.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/chauffeur")
def get_all_chauffeurs(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Chauffeur).all()

@app.put("/chauffeur/{ch_id}")
def update_chauffeur(ch_id: int, ch: schemas.ChauffeurUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = db.query(models.Chauffeur).filter(models.Chauffeur.id == ch_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Chauffeur non trouvé")
    obj.nom = ch.nom
    obj.salaire_base = ch.salaire_base
    obj.bus_id = ch.bus_id
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/chauffeur/{ch_id}")
def delete_chauffeur(ch_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = db.query(models.Chauffeur).filter(models.Chauffeur.id == ch_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Chauffeur non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Chauffeur supprimé"}

# -------------------
# CONTROLEUR
# -------------------
@app.post("/controleur")
def add_controleur(ctrl: schemas.ControleurCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = models.Controleur(**ctrl.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/controleur")
def get_all_controleurs(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Controleur).all()

@app.put("/controleur/{ctrl_id}")
def update_controleur(ctrl_id: int, ctrl: schemas.ControleurUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = db.query(models.Controleur).filter(models.Controleur.id == ctrl_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Controleur non trouvé")
    obj.nom = ctrl.nom
    obj.salaire_base = ctrl.salaire_base
    obj.bus_id = ctrl.bus_id
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/controleur/{ctrl_id}")
def delete_controleur(ctrl_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = db.query(models.Controleur).filter(models.Controleur.id == ctrl_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Controleur non trouvé")
    db.delete(obj)
    db.commit()
    return {"message": "Controleur supprimé"}

# -------------------
# DEPENSES DE FONCTIONNEMENT
# -------------------
@app.post("/depense")
def add_depense(dep: schemas.DepenseCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    obj = models.Depense(**dep.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/depense")
def get_all_depenses(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Depense).all()

# -------------------
# SALAIRES ET BENEFICES
# -------------------
@app.get("/salaire_total")
def salaire_total(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    chauffeurs = db.query(models.Chauffeur).all()
    controleurs = db.query(models.Controleur).all()
    total_chauffeurs = sum(c.salaire_base for c in chauffeurs)
    total_controleurs = sum(c.salaire_base for c in controleurs)
    return {
        "total_chauffeurs": total_chauffeurs,
        "total_controleurs": total_controleurs,
        "total_general": total_chauffeurs + total_controleurs
    }

@app.get("/finance/resume")
def resume(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    chauffeurs = db.query(models.Chauffeur).all()
    controleurs = db.query(models.Controleur).all()
    depenses = db.query(models.Depense).all()

    total_salaire = sum(c.salaire_base for c in chauffeurs) + sum(c.salaire_base for c in controleurs)
    total_depense = sum(d.montant for d in depenses)
    
    # Ici tu peux ajouter les recettes (billets)
    benefice = - (total_salaire + total_depense)

    return {
        "total_salaire": total_salaire,
        "total_depenses": total_depense,
        "benefice": benefice
    }

# -------------------
# HISTORIQUE COMPLET
# -------------------
@app.get("/historique")
def historique(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return {
        "bus": db.query(models.Bus).all(),
        "chauffeurs": db.query(models.Chauffeur).all(),
        "controleurs": db.query(models.Controleur).all(),
        "depenses": db.query(models.Depense).all()
    }

# -------------------
# CREATION DES TABLES
# -------------------
models.Base.metadata.create_all(bind=engine)
