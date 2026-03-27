from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
# Bus
class BusCreate(BaseModel):
    numero: str

class BusUpdate(BaseModel):
    numero: str

# Chauffeur
class ChauffeurCreate(BaseModel):
    nom: str
    salaire_base: float
    bus_id: int

class ChauffeurUpdate(BaseModel):
    nom: str
    salaire_base: float
    bus_id: int

# Controleur
class ControleurCreate(BaseModel):
    nom: str
    salaire_base: float
    bus_id: int

class ControleurUpdate(BaseModel):
    nom: str
    salaire_base: float
    bus_id: int

# Depense
class DepenseCreate(BaseModel):
    montant: float
    raison: str