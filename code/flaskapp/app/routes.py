import email
import datetime
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

from app import app, db, mail
from app.forms import LoginForm, RegistrationForm, AjoutAnimal, ChercherAnimal ,ContactForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Role, Animal, Employee ,Contact, Veterinaire, Soigneur, Service, Activite, Profil    

from flask_mail import Mail, Message

from werkzeug.security import generate_password_hash, check_password_hash



import json
from flask_restful import Api, Resource, reqparse
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
api = Api(app)

#______________________________________________________________________________
# LA TABLE USER 
class UserView(Resource):
    # AFFICHAGE TOUS USER
    def get(self):
        users = User.query.all()
        return {'User':list(x.json() for x in users)}

    # creer un copmte
    # AJOUTER USERS   
    def post(self):
        data = request.get_json()
        verifier = Role.query.filter_by(matricule=data['id']).first()
        if not verifier:
            return {'message':'You can\'t create a count1'},404
        else:  
            donne = verifier.json()
            role1 = donne['role']
            print(role1)
            role2 = data['posts'] 
            print(role2)
            def check_len(s1,s2):
                a = len(s1)
                b = len(s2)
                if (a>b):
                    print(s1, " is Longer")
                elif (a == b):
                    print("Equal Length")
                else:
                    print(s2, " is Longer")
            check_len(role1,role2)
            if (role1 == role2):  
                new_user = User(data['id'],data['username'],data['email'],generate_password_hash(data['password_hash']),data['posts'])
                db.session.add(new_user)
                db.session.commit()
                db.session.flush()
                return new_user.json(),201  
            else:
                return {'message':'You can\'t create a count'},404    

# connection
class Loginn(Resource):
   def post(self):
        data = request.get_json()
        new_user = User(data['id'],data['username'],data['email'],data['password_hash'],data['posts'])
        id = data["id"]
        username = data["username"]
        password = data["password_hash"]
        posts = data["posts"]
        email = data["email"]
        verifier = User.query.filter_by(id=id).first()
        if not verifier:
            return {'message':'You can\'t login'},404
        else:
            donne = verifier.json()
            usernamev = donne["username"]
            passwordv = donne["password_hash"]
            postsv = donne["posts"]
            emailv = donne["email"]
            check = check_password_hash(passwordv, password)
            print(check)
            if username != usernamev or not check or posts != postsv or email != emailv:
                return {'message':'You can\'t login'},404
            return new_user.json(),201       



class SingleUser(Resource):
    # AFFICHAGE UN SEUL USER
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            return user.json()
        return {'message':'User id not found'},404 

    # SUPPRESSION D'UN SEUL USER 
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'User not fount'},404

    # MODIFICATION D'UN SEUL USER 
    def put(self, id):
        data = request.get_json()
        user = User.query.filter_by(id=id).first()

        if user:
            user.id = data["id"]   
            user.username = data["username"]   
            user.email = data["email"]   
            user.password_hash = data["password_hash"]        
            user.posts = data["posts"]   
        else:
            user = User(id=id, **data)

        db.session.add(user)
        db.session.commit()

        return user.json()             



api.add_resource(Loginn, '/userr')   
api.add_resource(UserView, '/users') 
api.add_resource(SingleUser, '/user/<string:id>')          


#______________________________________________________________________________
# LA TABLE ROLE
class RoleView(Resource):  
    # AFFICHAGE TOUS ROLE
    def get(self):
        roles = Role.query.all()
        return {'Role':list(x.json() for x in roles)}

    # AJOUTER ROLE
    def post(self):
        data = request.get_json()
        new_role = Role(data['matricule'],data['nom'],data['prenom'],data['adresse'],data['tel'],data['role'])
        db.session.add(new_role)
        db.session.commit()
        db.session.flush()
        return new_role.json(),201  


class SingleRole(Resource):
    # AFFICHAGE UN SEUL ROLE
    def get(self, matricule): 
        role = Role.query.filter_by(matricule=matricule).first()
        if role:
            return role.json()
        return {'message':'Role id not found'},404 

    # SUPPRESSION D'UN SEUL ROLE 
    def delete(self, matricule):
        role = Role.query.filter_by(matricule=matricule).first()
        user = User.query.filter_by(id=matricule).first()
        if role:
            db.session.delete(role)
            db.session.commit()

            if user:
                db.session.delete(user)
                db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'role not fount'},404

    # MODIFICATION D'UN SEUL ROLE 
    def put(self, matricule): 
        data = request.get_json()
        role = Role.query.filter_by(matricule=matricule).first()

        if role:
            role.matricule = data["matricule"]   
            role.nom = data["nom"]   
            role.prenom = data["prenom"]   
            role.adresse = data["adresse"]        
            role.tel = data["tel"]   
            role.role = data["role"]   
        else:
            role = Role(matricule=matricule, **data)

        db.session.add(role)
        db.session.commit()

        return role.json()  


api.add_resource(RoleView, '/roles') 
api.add_resource(SingleRole, '/role/<string:matricule>')                    


# ----------------------------------------------------------------------------
#______________________________________________________________________________
# LA TABLE ACTIVITE
class ActiviteView(Resource):  
    # AFFICHAGE TOUS USEACTIVITER
    def get(self):
        activites = Activite.query.all()
        return {'Activite':list(x.json() for x in activites)}

    # AJOUTER ACTIVITE
    def post(self):
        data = request.get_json()
        new_activite = Activite(data['numActivite'],data['nomActivite'],data['dateActivite'],data['information'])
        db.session.add(new_activite)
        db.session.commit()
        db.session.flush()
        return new_activite.json(),201  


class SingleActivite(Resource):
    # AFFICHAGE UN SEUL ACTIVITE
    def get(self, numActivite): 
        activite = Activite.query.filter_by(numActivite=numActivite).first()
        if activite:
            return activite.json()
        return {'message':'Activite id not found'},404 

    # SUPPRESSION D'UN SEUL ACTIVITE 
    def delete(self, numActivite):
        activite = Activite.query.filter_by(numActivite=numActivite).first()
        if activite:
            db.session.delete(activite)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'activite not fount'},404

    # MODIFICATION D'UN SEUL ACTIVITE 
    def put(self, numActivite): 
        data = request.get_json()
        activite = Activite.query.filter_by(numActivite=numActivite).first()

        if activite:
            activite.numActivite = data["numActivite"]   
            activite.nomActivite = data["nomActivite"]   
            activite.dateActivite = data["dateActivite"]   
            activite.information = data["information"]        
  
        else:
            activite = Activite(numActivite=numActivite, **data)

        db.session.add(activite)
        db.session.commit()

        return activite.json()  


api.add_resource(ActiviteView, '/activites') 
api.add_resource(SingleActivite, '/activite/<int:numActivite>')    


# ----------------------------------------------------------------------------
#______________________________________________________________________________
# LA TABLE SERVICE
class ServiceView(Resource):  
    # AFFICHAGE TOUS SERVICE
    def get(self):
        services = Service.query.all()
        return {'Service':list(x.json() for x in services)}

    # AJOUTER SERVICE
    def post(self):
        data = request.get_json()
        new_service = Service(data['numService'],data['nomService'],data['nbrZone'],data['description'],data['adresse'])
        db.session.add(new_service)
        db.session.commit()
        db.session.flush()
        return new_service.json(),201  


class SingleService(Resource):
    # AFFICHAGE UN SEUL SERVICE
    def get(self, numService): 
        service = Service.query.filter_by(numService=numService).first()
        if service:
            return service.json()
        return {'message':'Service id not found'},404 

    # SUPPRESSION D'UN SEUL SERVICE 
    def delete(self, numService):
        service = Service.query.filter_by(numService=numService).first()
        if service:
            db.session.delete(service)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'activite not fount'},404

    # MODIFICATION D'UN SEUL SERVICE 
    def put(self, numService): 
        data = request.get_json()
        service = Service.query.filter_by(numService=numService).first()

        if service:
            service.numService = data["numService"]   
            service.nomService = data["nomService"]   
            service.nbrZone = data["nbrZone"]   
            service.description = data["description"]     
            service.adresse = data["adresse"]        
  
        else:
            service = Service(numService=numService, **data)

        db.session.add(service)
        db.session.commit()

        return service.json()          

api.add_resource(ServiceView, '/services') 
api.add_resource(SingleService, '/service/<int:numService>')    



# ----------------------------------------------------------------------------
#______________________________________________________________________________
# LA TABLE employe
class EmployeView(Resource):  
    # AFFICHAGE TOUS SERVICE
    def get(self):
        employes = Employee.query.all()
        return {'Employe':list(x.json() for x in employes)}

    # AJOUTER SERVICE
    def post(self):
        data = request.get_json()
        new_employe = Employee(data['mat_emp'],data['nom_emp'],data['prenom_emp'],data['adress_emp'],data['date_naissance'],data['date_recrutement'],data['num_pieceId'],data['num_equipe'],data['structure'],data['num_zone'])
        db.session.add(new_employe)
        db.session.commit()
        db.session.flush()
        return new_employe.json(),201 

class SingleEmploye(Resource):
    # AFFICHAGE UN SEUL SERVICE
    def get(self, mat_emp): 
        employe = Employee.query.filter_by(mat_emp=mat_emp).first()
        if employe:
            return employe.json()
        return {'message':'Employe id not found'},404 

    # SUPPRESSION D'UN SEUL SERVICE 
    def delete(self, mat_emp):
        employe = Employee.query.filter_by(mat_emp=mat_emp).first()
        if employe:
            db.session.delete(employe)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'activite not fount'},404

    # MODIFICATION D'UN SEUL SERVICE 
    def put(self, mat_emp): 
        data = request.get_json()
        employe = Employee.query.filter_by(mat_emp=mat_emp).first()
    
        if employe:
            employe.mat_emp = data["mat_emp"]   
            employe.nom_emp = data["nom_emp"]   
            employe.prenom_emp = data["prenom_emp"]   
            employe.adress_emp = data["adress_emp"]     
            employe.date_naissance = data["date_naissance"]  
            employe.date_recrutement = data["date_recrutement"]   
            employe.num_pieceId = data["num_pieceId"]   
            employe.num_equipe = data["num_equipe"]   
            employe.structure = data["structure"]     
            employe.num_zone = data["num_zone"]        
  
        else:
            employe = Employee(mat_emp=mat_emp, **data)

        db.session.add(employe)
        db.session.commit()

        return employe.json()        


api.add_resource(EmployeView, '/employes') 
api.add_resource(SingleEmploye, '/employe/<string:mat_emp>')    


# ----------------------------------------------------------------------------
#______________________________________________________________________________
# LA TABLE ANIMAL
class AnimalView(Resource):  
    # AFFICHAGE TOUS ANIMAL
    def get(self):
        animals = Animal.query.all()
        return {'Animal':list(x.json() for x in animals)}

    # AJOUTER ANIMAL
    def post(self):
        data = request.get_json()
        new_animal = Animal(data['codeAnimal'],data['espece'],data['famille'],data['embranchement'],data['race'],data['couleur'],data['pelage'],data['sexe'],data['poids'],data['taille'],data['origine'],data['DateNais'],data['age'],data['DateDeses'],data['SignePart'],data['NumZone'],data['NumEnclo'])
        db.session.add(new_animal)
        db.session.commit()    

        my_data2 = Veterinaire(0, 0, '', '', '', data['codeAnimal'])
        db.session.add(my_data2)
        db.session.commit()

        my_data3 = Soigneur(0.0, 0.0, '', data['codeAnimal'])
        db.session.add(my_data3)
        db.session.commit()
    
        db.session.flush()
        return new_animal.json(),201 


class SingleAnimal(Resource):
    # AFFICHAGE UN SEUL SERVICE
    def get(self, codeAnimal): 
        animal = Animal.query.filter_by(codeAnimal=codeAnimal).first()
        if animal:
            return animal.json()
        return {'message':'Animal id not found'},404 

    # SUPPRESSION D'UN SEUL ANIMAL 
    def delete(self, codeAnimal):
        animal = Animal.query.filter_by(codeAnimal=codeAnimal).first()
        animal2 = Veterinaire.query.filter_by(animal_codeAnimal=codeAnimal).first()
        animal3 = Soigneur.query.filter_by(soigneur_codeAnimal=codeAnimal).first()
        if animal:
            db.session.delete(animal)
            db.session.commit()

            db.session.delete(animal2)
            db.session.commit()

            db.session.delete(animal3)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'Animal not fount'},404

    # MODIFICATION D'UN SEUL SERVICE 
    def put(self, codeAnimal): 
        data = request.get_json()
        animal = Animal.query.filter_by(codeAnimal=codeAnimal).first()

        if animal:
            animal.codeAnimal = data["codeAnimal"]   
            animal.espece = data["espece"]   
            animal.famille = data["famille"]   
            animal.embranchement = data["embranchement"]     
            animal.race = data["race"]        

            animal.couleur = data["couleur"]   
            animal.pelage = data["pelage"]   
            animal.sexe = data["sexe"]   
            animal.poids = data["poids"]     
            animal.taille = data["taille"]  

            animal.origine = data["origine"]   
            animal.DateNais = data["DateNais"]   
            animal.age = data["age"]   
            animal.DateDeses = data["DateDeses"]     
            animal.SignePart = data["SignePart"]   
            animal.NumZone = data["NumZone"]     
            animal.NumEnclo = data["NumEnclo"]        
  
        else:
            animal = Animal(codeAnimal=codeAnimal, **data)

        db.session.add(animal)
        db.session.commit()

        return animal.json()                   

api.add_resource(AnimalView, '/animals') 
api.add_resource(SingleAnimal, '/animal/<string:codeAnimal>')    


#______________________________________________________________________________
# LA TABLE VETERINAIRE
class VeterinaireView(Resource):  
    # AFFICHAGE TOUS SERVICE
    def get(self):
        veterinaires = Veterinaire.query.all()
        return {'Veterinaire':list(x.json() for x in veterinaires)}

    # AJOUTER SERVICE
    def post(self):
        data = request.get_json()
        new_animal = Veterinaire(data['animal_codeAnimal'],data['qteau'],data['qtenouriture'],data['natureNouri'],data['examenGeneral'],data['ispectionRepertoirCardial'])
        db.session.add(new_animal)
        db.session.commit()
        db.session.flush()
        return new_animal.json(),201 

class SingleVeterinaire(Resource):
    # AFFICHAGE UN SEUL SERVICE
    def get(self, animal_codeAnimal): 
        animal = Veterinaire.query.filter_by(animal_codeAnimal=animal_codeAnimal).first()
        if animal:
            return animal.json()
        return {'message':'Animal id not found'},404 

    # SUPPRESSION D'UN SEUL SERVICE 
    def delete(self, animal_codeAnimal):
        animal = Veterinaire.query.filter_by(animal_codeAnimal=animal_codeAnimal).first()
        if animal:
            db.session.delete(animal)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'activite not fount'},404

    # MODIFICATION D'UN SEUL SERVICE 
    def put(self, animal_codeAnimal): 
        data = request.get_json()
        animal = Veterinaire.query.filter_by(animal_codeAnimal=animal_codeAnimal).first()
    
        if animal:
            animal.animal_codeAnimal = data["animal_codeAnimal"]   
            animal.qteau = data["qteau"]   
            animal.qtenouriture = data["qtenouriture"]   
            animal.natureNouri = data["natureNouri"]
            animal.examenGeneral = data["examenGeneral"]
            animal.ispectionRepertoirCardial = data["ispectionRepertoirCardial"]           
  
        else:
            animal = Veterinaire(animal_codeAnimal=animal_codeAnimal, **data)

        db.session.add(animal)
        db.session.commit()

        return animal.json()        


api.add_resource(VeterinaireView, '/veterinaires') 
api.add_resource(SingleVeterinaire, '/veterinaire/<string:animal_codeAnimal>')   



#______________________________________________________________________________
# LA TABLE SOIGNEUR
class SoigneurView(Resource):  
    # AFFICHAGE TOUS SERVICE
    def get(self):
        soigneurs = Soigneur.query.all()
        return {'Soigneur':list(x.json() for x in soigneurs)}

    # AJOUTER SERVICE
    def post(self):
        data = request.get_json()
        new_animal = Soigneur(data['soigneur_codeAnimal'],data['qteauConsomme'],data['qtenouritureConsomme'],data['remarque'])
        db.session.add(new_animal)
        db.session.commit()
        db.session.flush()
        return new_animal.json(),201 

class SingleSoigneur(Resource):

    def get(self, soigneur_codeAnimal): 
        animal = Soigneur.query.filter_by(soigneur_codeAnimal=soigneur_codeAnimal).first()
        if animal:
            return animal.json()
        return {'message':'Animal id not found'},404 
   

    # SUPPRESSION D'UN SEUL SERVICE 
    def delete(self, soigneur_codeAnimal):
        animal = Soigneur.query.filter_by(matsoigneur_codeAnimal_emp=soigneur_codeAnimal).first()
        if animal:
            db.session.delete(animal)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'activite not fount'},404

    # MODIFICATION D'UN SEUL SERVICE 
    def put(self, soigneur_codeAnimal): 
        data = request.get_json()
        animal = Soigneur.query.filter_by(soigneur_codeAnimal=soigneur_codeAnimal).first()
    
        if animal:
            animal.soigneur_codeAnimal = data["soigneur_codeAnimal"]   
            animal.qteauConsomme = data["qteauConsomme"]   
            animal.qtenouritureConsomme = data["qtenouritureConsomme"]   
            animal.remarque = data["remarque"]           
  
        else:
            animal = Soigneur(soigneur_codeAnimal=soigneur_codeAnimal, **data)

        db.session.add(animal)
        db.session.commit()

        return animal.json()        


api.add_resource(SoigneurView, '/soigneurs') 
api.add_resource(SingleSoigneur, '/soigneur/<string:soigneur_codeAnimal>')   

class ContactView(Resource): 
    # AFFICHAGE TOUS MSG
    def get(self):
        message = Contact.query.all()
        return {'Contact':list(x.json() for x in message)}

    # AJOUTER MSG CONTACT
    def post(self):
        data = request.get_json()
        new_contact = Contact(data['email'],data['nom'],data['tel'],data['message'])
        msg = Message("Message d'un visiteur", sender=data['email'], recipients=["pzoologique@gmail.com"])
        msg.body = "Message de " +f"{data['nom']}"+ "\n\n"+ "email: " +f"{data['email']}" +"\n\n"+ "Tel: " +f"{data['tel']}"+ "\n\n"+ "Le message:"+ "\n\n" +f"{data['message']}"
        mail.send(msg)
        return new_contact.json(),201 

api.add_resource(ContactView, '/contact') 


#______________________________________________________________________________
# LA TABLE PROFIL
class ProfilView(Resource):  
    # AFFICHAGE TOUS ROLE
    def get(self):
        profils = Profil.query.all()
        return {'Profil':list(x.json() for x in profils)}

    # AJOUTER ROLE
    def post(self):
        data = request.get_json()
        new_profil = Profil(data['Firstname'],data['Lastname'],data['email'],data['phone'],data['street'],data['city'],data['role'])
        db.session.add(new_profil)
        db.session.commit()
        db.session.flush()
        return new_profil.json(),201  


class SingleProfil(Resource):
    # AFFICHAGE UN SEUL ROLE
    def get(self, email): 
        profil = Profil.query.filter_by(email=email).first()
        if profil:
            return profil.json()
        return {'message':'Profil id not found'},404 

    # SUPPRESSION D'UN SEUL ROLE 
    def delete(self, email):
        profil = Profil.query.filter_by(email=email).first()
        if profil:
            db.session.delete(profil)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'role not fount'},404

    # MODIFICATION D'UN SEUL ROLE 
    def put(self, email): 
        data = request.get_json()
        profil = Profil.query.filter_by(email=email).first()

        if profil:
            profil.email = data["email"]   
            profil.Firstname = data["Firstname"]   
            profil.Lastname = data["Lastname"]   
            profil.phone = data["phone"]        
            profil.street = data["street"]   
            profil.city = data["city"]
            profil.role = data["role"]   
        else:
            profil = Profil(email=email, **data)

        db.session.add(profil)
        db.session.commit()

        return profil.json()  



api.add_resource(ProfilView, '/profils') 
api.add_resource(SingleProfil, '/profil/<string:email>')                    



