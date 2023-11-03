from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

import json


class User(UserMixin, db.Model):
    __tablename__='user'

    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.Column(db.String(100))

    def __init__(self, id, username, email, password_hash, posts):

        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.posts = posts

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def json(self):
        return{"id":self.id, "username":self.username, "email":self.email, "password_hash":self.password_hash, "posts":self.posts}    


class Role(UserMixin, db.Model):
    __tablename__='role'

    matricule=db.Column(db.String(100), primary_key=True)
    nom=db.Column(db.String(64))
    prenom=db.Column(db.String(64))
    adresse=db.Column(db.String(100))
    tel=db.Column(db.Integer())
    role = db.Column(db.String(100))

    def __init__(self, matricule, nom, prenom, adresse, tel, role):
 
        self.matricule=matricule
        self.nom = nom
        self.prenom=prenom
        self.adresse=adresse
        self.tel=tel
        self.role=role

    def json(self):
        return{"matricule":self.matricule, "nom":self.nom, "prenom":self.prenom, "adresse":self.adresse, "tel":self.tel, "role":self.role}    
    


class Animal(UserMixin, db.Model):
    codeAnimal = db.Column(db.String(100), primary_key=True)
    espece = db.Column(db.String(100))
    famille = db.Column(db.String(100))
    embranchement = db.Column(db.String(100))
    race = db.Column(db.String(100))
    couleur = db.Column(db.String(20))
    pelage = db.Column(db.String(100))
    sexe = db.Column(db.String(20))
    poids = db.Column(db.Float())
    taille = db.Column(db.Float())
    origine = db.Column(db.String(100))
    DateNais = db.Column(db.String(100))
    age = db.Column(db.Integer())
    DateDeses = db.Column(db.String(100))
    SignePart = db.Column(db.String(500))
    NumZone = db.Column(db.Integer())
    NumEnclo = db.Column(db.Integer())
    
    veterinaire = db.relationship('Veterinaire', backref='author', cascade="all, delete-orphan", lazy='dynamic')
    soigneur = db.relationship('Soigneur', backref='author', cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, codeAnimal, espece, famille, embranchement, race, couleur, pelage, sexe, poids, taille, origine, DateNais, age, DateDeses, SignePart, NumZone, NumEnclo):
 
        self.codeAnimal=codeAnimal
        self.espece = espece
        self.famille=famille
        self.embranchement=embranchement
        self.race=race
        self.couleur=couleur
        self.pelage=pelage
        self.sexe = sexe
        self.poids=poids
        self.taille=taille
        self.origine=origine
        self.DateNais=DateNais
        self.age = age
        self.DateDeses=DateDeses
        self.SignePart=SignePart
        self.NumZone=NumZone
        self.NumEnclo=NumEnclo

    def json(self):
        return{"codeAnimal":self.codeAnimal, "espece":self.espece, "famille":self.famille, "embranchement":self.embranchement, "race":self.race, "couleur":self.couleur, "pelage":self.pelage, "sexe":self.sexe, "poids":self.poids, "taille":self.taille, "origine":self.origine, "DateNais":self.DateNais, "age":self.age, "DateDeses":self.DateDeses, "SignePart":self.SignePart, "NumZone":self.NumZone, "NumEnclo":self.NumEnclo}    
    


class Veterinaire(UserMixin, db.Model):
    __tablename__='veterinaire'
   
    qteau = db.Column(db.Integer())
    qtenouriture = db.Column(db.Integer())
    natureNouri = db.Column(db.String(100))
    examenGeneral = db.Column(db.String(100))
    ispectionRepertoirCardial = db.Column(db.String(200))
    animal_codeAnimal = db.Column(db.String(100), db.ForeignKey('animal.codeAnimal'), primary_key=True)
    #tickermatch = db.relationship('Animal', backref='share', cascade="all, delete-orphan", lazy="joined")

    def __init__(self, qteau, qtenouriture, natureNouri, examenGeneral, ispectionRepertoirCardial, animal_codeAnimal):

        self.qteau = qteau
        self.qtenouriture = qtenouriture
        self.natureNouri = natureNouri
        self.examenGeneral = examenGeneral
        self.ispectionRepertoirCardial = ispectionRepertoirCardial
        self.animal_codeAnimal = animal_codeAnimal

    def json(self):
        return{"qteau":self.qteau, "qtenouriture":self.qtenouriture, "natureNouri":self.natureNouri, "examenGeneral":self.examenGeneral, "ispectionRepertoirCardial":self.ispectionRepertoirCardial, "animal_codeAnimal":self.animal_codeAnimal}    
        


class Employee(UserMixin, db.Model):
    __tablename__='employee'

    mat_emp=db.Column(db.String(30), primary_key=True)
    nom_emp=db.Column(db.String(60))
    prenom_emp=db.Column(db.String(60))
    adress_emp=db.Column(db.String(100))
    date_naissance=db.Column(db.String(100))
    date_recrutement=db.Column(db.String(100))
    num_pieceId=db.Column(db.Integer())
    num_equipe=db.Column(db.Integer())
    structure=db.Column(db.String())
    num_zone=db.Column(db.Integer())


    def __init__(self, mat_emp, nom_emp, prenom_emp, adress_emp,date_naissance, date_recrutement,numpieceId , num_equipe,structure,  num_zone):
 
        self.mat_emp = mat_emp
        self.nom_emp = nom_emp
        self.prenom_emp=prenom_emp
        self.adress_emp=adress_emp
        self.date_naissance=date_naissance
        self.date_recrutement=date_recrutement
        self.num_pieceId=numpieceId
        self.num_equipe=num_equipe
        self.structure=structure
        self.num_zone=num_zone

    def json(self):
        return{"mat_emp":self.mat_emp, "nom_emp":self.nom_emp, "prenom_emp":self.prenom_emp, "adress_emp":self.adress_emp, "date_naissance":self.date_naissance, "date_recrutement":self.date_recrutement, "num_pieceId":self.num_pieceId, "num_equipe":self.num_equipe, "structure":self.structure, "num_zone":self.num_zone}    
    


class Soigneur(UserMixin, db.Model):
    qteauConsomme = db.Column(db.Float())
    qtenouritureConsomme = db.Column(db.Float())
    remarque = db.Column(db.String(500))
    soigneur_codeAnimal = db.Column(db.String(100), db.ForeignKey('animal.codeAnimal'), primary_key=True)


    def __init__(self, qteauConsomme, qtenouritureConsomme, remarque, soigneur_codeAnimal):
        self.qteauConsomme = qteauConsomme
        self.qtenouritureConsomme = qtenouritureConsomme
        self.remarque = remarque
        self.soigneur_codeAnimal = soigneur_codeAnimal

    def json(self):
        return{"qteauConsomme":self.qteauConsomme, "qtenouritureConsomme":self.qtenouritureConsomme, "remarque":self.remarque, "soigneur_codeAnimal":self.soigneur_codeAnimal}    
        



class Contact(UserMixin, db.Model):
    email=db.Column(db.String(60), primary_key=True)
    nom=db.Column(db.String(60))
    tel=db.Column(db.String(60))
    message=db.Column(db.String(200))

    def __init__(self, email, nom, tel, message):
        self.email=email
        self.nom= nom
        self.tel = tel
        self.message=message

    def json(self):
        return{"email":self.email, "nom":self.nom, "tel":self.tel, "message":self.message}    
           


class Service(UserMixin, db.Model):
    numService=db.Column(db.Integer(), primary_key=True)
    nomService=db.Column(db.String(60))
    nbrZone=db.Column(db.Integer())
    description=db.Column(db.String(400))
    adresse=db.Column(db.String(100))

    def __init__(self, numService, nomService, nbrZone, description, adresse):
        self.numService=numService
        self.nomService= nomService
        self.nbrZone = nbrZone
        self.description =description
        self.adresse=adresse

    def json(self):
        return{"numService":self.numService, "nomService":self.nomService, "nbrZone":self.nbrZone, "description":self.description, "adresse":self.adresse}    




class Activite(UserMixin, db.Model):
    __tablename__='activite'

    numActivite=db.Column(db.Integer(), primary_key=True)
    nomActivite=db.Column(db.String(100))
    dateActivite=db.Column(db.String(100))
    information=db.Column(db.String(400))
    

    def __init__(self, numActivite, nomActivite, dateActivite, information):
        self.numActivite=numActivite
        self.nomActivite= nomActivite
        self.dateActivite = dateActivite
        self.information=information 
   
    def json(self):
        return {"numActivite":self.numActivite, "nomActivite":self.nomActivite, "dateActivite":self.dateActivite, "information":self.information}  


class Profil(UserMixin, db.Model):
    __tablename__='profil'
    
    Firstname=db.Column(db.String(100))
    Lastname=db.Column(db.String(100))
    email=db.Column(db.String(100), primary_key=True)
    phone=db.Column(db.String(100))
    street=db.Column(db.String(100))
    city=db.Column(db.String(100))
    role=db.Column(db.String(100))


    def __init__(self, Firstname, Lastname, email, phone, street, city, role):
        self.Firstname=Firstname
        self.Lastname= Lastname
        self.email = email
        self.phone=phone
        self.street=street
        self.city=city
        self.role=role

    def json(self):
        return {"Firstname":self.Firstname, "Lastname":self.Lastname, "email":self.email, "phone":self.phone, "street":self.street, "city":self.city, "role":self.role}  






@login.user_loader
def load_user(id):
    return User.query.get(str(id))

