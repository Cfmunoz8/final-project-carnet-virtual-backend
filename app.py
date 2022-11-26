from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from models import db, Patient, Clinical_record
from datetime import date, datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///final-project.db"
db.init_app(app)
CORS(app)
Migrate(app, db)


@app.route("/")
def home():
    return "prueba exitosa"

@app.route("/patient_list", methods=["GET"])
def patient_list():
    patient = Patient.query.all()
    patient_serialized = list(map( lambda patient: patient.serialize(), patient))
    return jsonify(patient_serialized)

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


@app.route("/get_clinical_record", methods=["GET"])
def get_clinical_record():
    clinical_record = Clinical_record.query.all()
    clinical_record_serialized = list(map( lambda clinical_record: clinical_record.serialize(), clinical_record))
    return jsonify(clinical_record_serialized)


@app.route("/create_clinical_record", methods=["POST"])

def create_clinical_record():
    clinical_record = Clinical_record()
    clinical_record.program = request.json.get("program")
    registration_date = request.json.get("registration_date")
    clinical_record.registration_date = date.fromisoformat(registration_date)
    clinical_record.barthel_index = request.json.get("barthel_index")
    clinical_record.zarit_scale_caregiver = request.json.get("zarit_scale_caregiver")
    clinical_record.patient_id = request.json.get("patient_id")

    db.session.add(clinical_record)
    db.session.commit()

    return "ficha creada correctamente"



app.run(host="localhost", port=8080)