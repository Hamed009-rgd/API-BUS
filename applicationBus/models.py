from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)  # le mot de passe sera haché
    
class Bus(Base):
    __tablename__ = "bus"
    id = Column(Integer, primary_key=True)
    numero = Column(String, unique=True)

class Chauffeur(Base):
    __tablename__ = "chauffeurs"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    salaire_base = Column(Float)  # salaire mensuel de base
    bus_id = Column(Integer)      # bus assigné

class Controleur(Base):
    __tablename__ = "controleurs"
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    salaire_base = Column(Float)
    bus_id = Column(Integer)

class Depense(Base):
    __tablename__ = "depenses"
    id = Column(Integer, primary_key=True)
    montant = Column(Float)
    raison = Column(String)