import os
from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, Patient
from models import db, Professional


BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR,"final-project.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ENV"] = "development"
app.config["SECRET_KEY"] = "super_secret_key"
app.config["JWT_SECRET_KEY"] = "super_jwt_key"

db.init_app(app)
CORS(app)
Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@app.route("/")
def home():
    return "prueba exitosa"

@app.route("/patient_list", methods=["GET"])
def patient_list():
    patient = Patient.query.all()
    patient_serialized = list(map( lambda patient: patient.serialize(), patient))
    return jsonify(patient_serialized)


@app.route("/professionals")   
@jwt_required()
def professionals():
    all_professionals = Professional.query.all()
    all_professionals = list(map(lambda professional: professional.serialize(),all_professionals ))
    return jsonify({
        "data": all_professionals
    })



@app.route("/login_professional", methods =["POST"])
def login_professional ():
    password = request.json.get("password")
    rut = request.json.get("rut")

    found_professional =Professional.query.filter_by(rut=rut).first()

    if found_professional is None:
        return jsonify({
            "msg":"professional not found plaease create professional"
        }), 404


    if bcrypt.check_password_hash(found_professional.password,password):
        access_token = create_access_token (identity=rut)
        return jsonify ({
            "access_token": access_token,
            "data": found_professional.serialize(),
            "success": True
        }), 200

    else:
        return jsonify({
            "msg": "password is invalid"
        })    



@app.route("/add_professional", methods=["POST"])
def add_professional ():
    professional = Professional()
    name = request.json.get("name")
    lastname = request.json.get("lastname")
    rut = request.json.get("rut")
    role = request.json.get("role")
    email = request.json.get("email")
    password = request.json.get("password")

    found_professional_rut = Professional.query.filter_by(rut=rut).first()
    
    if found_professional_rut is not None:
        return jsonify({
            "msg" :"Rut is already in use"
        }), 400

    found_professional_email = Professional.query.filter_by(email=email).first()
    
    if found_professional_email is not None:
        return jsonify({
            "msg" :"Email is already in use"
        }), 400   

    professional.name = name
    professional.lastname = lastname
    professional.rut = rut
    professional.role = role
    professional.email = email
    password_hash = bcrypt.generate_password_hash(password)
    professional.password = password_hash 

    db.session.add(professional)
    db.session.commit()

    return jsonify({
        "msg":"success creating professional"
    }), 200


@app.route("/add_patient", methods=["POST"])
def add_patient():
    patient = Patient()
    patient.name = request.json.get("name")
    patient.lastname = request.json.get("lastname")
    patient.rut = request.json.get("rut")
    patient.age = request.json.get("age")
    patient.gender = request.json.get("gender")
    patient.birth_date = request.json.get("birth_date")
    patient.email = request.json.get("email")
    patient.password = request.json.get("password")
    patient.address = request.json.get("address")
    patient.phone_number = request.json.get("phone_number")
    patient.alive = request.json.get("alive")

    db.session.add(patient)
    db.session.commit()

    return "paciente añadido correctamente"

@app.route("/update_patient/<int:id>", methods=["PUT"])
def update_patient(id):
    patient = Patient.query.get(id)
    patient.name = request.json.get("name")
    patient.lastname = request.json.get("lastname")
    patient.rut = request.json.get("rut")
    patient.age = request.json.get("age")
    patient.gender = request.json.get("gender")
    patient.birth_date = request.json.get("birth_date")
    patient.email = request.json.get("email")
    patient.password = request.json.get("password")
    patient.address = request.json.get("address")
    patient.phone_number = request.json.get("phone_number")
    patient.alive = request.json.get("alive")

    db.session.add(patient)
    db.session.commit()

    return "paciente actualizado correctamente"

@app.route("/update_patient_alive/<int:id>", methods=["PUT"])
def update_patient_alive(id):
    patient = Patient.query.get(id)
    patient.alive = request.json.get("alive")

    db.session.add(patient)
    db.session.commit()

    return "se ha cambiado el estado del paciente a fallecido"

@app.route("/delete_patient/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get(id)
    
    db.session.delete(patient)
    db.session.commit()

    return "paciente eliminado correctamente"

if __name__ == "__main__":
    app.run(host="localhost", port=8080)
