
import os
from flask import Flask, jsonify, request
from flask_cors import CORS 
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
from models import db,Professional, Patient, Clinical_record, Caregiver, Drug, Control,Habit,Pathology,Surgery,Alergy
from datetime import date, datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

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

@app.route("/login_patient", methods=["POST"])
def login_patient():
    password = request.json.get("password")
    rut = request.json.get("rut")

    found_patient = Patient.query.filter_by(rut=rut).first()

    if found_patient is None:
        return jsonify ({
            "msg": "contraseña o rut invalido"
        }), 404
    
    if bcrypt.check_password_hash(found_patient.password, password):
        access_token = create_access_token(identity=found_patient.id)
        return jsonify({
            "access_token": access_token,
            "data": found_patient.serialize(),
            "success": True
        }), 200
    
    else:
        return jsonify ({
            "msg": "contraseña o rut invalido"
        })


@app.route("/patient_list", methods=["GET"])
@jwt_required()
def patient_list():
    professional_id = get_jwt_identity()
    
    patient = Patient.query.all()
    patient_serialized = list(map( lambda patient: patient.serialize(), patient))
    return jsonify(patient_serialized)

@app.route("/patient/<int:id>", methods=["GET"])
@jwt_required()
def patient(id):
    patient = Patient.query.get(id)
    patient_serialized = patient.serialize()
    return jsonify(patient_serialized)


@app.route("/professionals")   
@jwt_required()
def professionals():
    professional = Professional.query.all()
    professional_serialized = list(map(lambda professional: professional.serialize(), professional))
    return jsonify(professional_serialized)



@app.route("/login_professional", methods =["POST"])

def login_professional ():
    password = request.json.get("password")
    rut = request.json.get("rut")

    found_professional = Professional.query.filter_by(rut=rut).first()

    if found_professional is None:
        return jsonify({
            "msg":"rut o contraseña incorrecta"
        }), 404


    if bcrypt.check_password_hash(found_professional.password, password):
        access_token = create_access_token (identity=found_professional.id)
        return jsonify ({
            "access_token": access_token,
            "data": found_professional.serialize(),
            "success": True
        }), 200

    else:
        return jsonify({
            "msg": "rut o contraseña incorrecta"
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
    email = request.json.get("email")
    rut = request.json.get("rut")
    password = request.json.get("password")

    found_patient = Patient.query.filter_by(rut=rut).first()

    if found_patient is not None:
        return jsonify({
            "msg": "Ya existe un paciente ingresado con este rut"
        }), 400
    
    found_email = Patient.query.filter_by(email=email).first()

    if found_email is not None:
        return jsonify({
            "msg": "Ya existe un paciente ingresado con este email"
        }), 400

    patient.name = request.json.get("name")
    patient.lastname = request.json.get("lastname")
    patient.rut = rut
    patient.age = request.json.get("age")
    patient.gender = request.json.get("gender")
    patient.birth_date = request.json.get("birth_date")
    patient.email = email
    password_hash = bcrypt.generate_password_hash(password)
    patient.password = password_hash
    patient.address = request.json.get("address")
    patient.phone_number = request.json.get("phone_number")
    patient.alive = request.json.get("alive")

    db.session.add(patient)
    db.session.commit()

    return jsonify({
        "msg": "paciente añadido correctamente"
        }), 200

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


@app.route("/get_caregivers", methods=["GET"])
def get_caregivers():
    caregiver = Caregiver.query.all()
    caregiver_serialized = list(map( lambda caregiver: caregiver.serialize(), caregiver))
    return jsonify(caregiver_serialized)

@app.route("/add_caregiver", methods=["POST"])
def add_caregiver():
    caregiver = Caregiver()
    patient_id = request.json.get("patient_id")

    found_patient = Patient.query.filter_by(id=patient_id).first()

    if found_patient is None:
        return jsonify({
            "msg": "no existe este paciente"
        }), 400

    found_caregiver = Caregiver.query.filter_by(patient_id=patient_id).first()

    if found_caregiver is not None:
        return jsonify({
            "msg": "este paciente ya tiene un cuidador asignado"
        }), 400

    caregiver.name = request.json.get("name")
    caregiver.lastname = request.json.get("lastname")
    caregiver.rut = request.json.get("rut")
    caregiver.address = request.json.get("address")
    caregiver.patient_id = patient_id

    db.session.add(caregiver)
    db.session.commit()

    return jsonify({
        "msg": "cuidador añadido correctamente"
    }), 200


@app.route("/get_caregiver", methods=["GET"])
@jwt_required()
def get_caregiver():
    patient_id = get_jwt_identity()
    caregiver = Caregiver.query.get(patient_id)
    return jsonify(caregiver.serialize())


@app.route("/get_clinical_records", methods=["GET"])
def get_clinical_records():
    clinical_record = Clinical_record.query.all()
    clinical_record_serialized = list(map( lambda clinical_record: clinical_record.serialize(), clinical_record))
    return jsonify(clinical_record_serialized)


@app.route("/get_clinical_record", methods=["GET"])
@jwt_required()
def get_clinical_record():
    patient_id = get_jwt_identity()
    clinical_record = Clinical_record.query.get(patient_id)
    clinical_record_serialized = clinical_record.serialize()
    return jsonify(clinical_record_serialized)

@app.route("/create_clinical_record", methods=["POST"])
def create_clinical_record():
    clinical_record = Clinical_record()
    patient_id = request.json.get("patient_id")

    found_patient = Patient.query.filter_by(id=patient_id).first()

    if found_patient is None:
        return jsonify({
            "msg": "no existe este paciente"
        }), 400

    found_clinical_record = Clinical_record.query.filter_by(patient_id=patient_id).first()

    if found_clinical_record is not None:
        return jsonify({
            "msg": "este paciente ya tiene una ficha clínica creada"
        }), 400

    clinical_record.program = request.json.get("program")
    registration_date = request.json.get("registration_date")
    clinical_record.registration_date = date.fromisoformat(registration_date)
    clinical_record.barthel_index = request.json.get("barthel_index")
    clinical_record.zarit_scale_caregiver = request.json.get("zarit_scale_caregiver")
    clinical_record.patient_id = patient_id

    db.session.add(clinical_record)
    db.session.commit()

    return jsonify({
        "msg": "ficha creada correctamente"
    }), 200

@app.route("/add_drug", methods=["POST"])
def create_drug():
    drug = Drug()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    drug.name = request.json.get("name")
    drug.posology = request.json.get("posology")
    drug.clinical_record_id = clinical_record_id

    db.session.add(drug)
    db.session.commit()

    return jsonify({
        "msg": "medicamento añadido correctamente"
    }), 200

@app.route("/alldrugs", methods=["GET"])
def alldrugs():
    drug = Drug.query.all()
    drug_serialized = list(map( lambda drug: drug.serialize(), drug))
    return jsonify(drug_serialized)


@app.route("/drugs", methods=["GET"])
@jwt_required()
def drugs():
    patient_id = get_jwt_identity()
    drug = Drug.query.filter_by(clinical_record_id=patient_id).all()
    drug_serialized = list(map( lambda drug: drug.serialize(), drug))
    return jsonify(drug_serialized)


@app.route("/delete_drug/<int:id>", methods=["DELETE"])
def delete_drug(id):
    drug = Drug.query.get(id)
    
    db.session.delete(drug)
    db.session.commit()

    return jsonify({
        "msg": "medicamento eliminado correctamente"
    }), 200


@app.route("/create_control", methods=["POST"])
def create_control():
    control = Control()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    control.reason = request.json.get("reason")
    control.description = request.json.get("description")
    control.indications = request.json.get("indications")
    date_of_control = request.json.get("date_of_control")
    control.date_of_control = date.fromisoformat(date_of_control)
    control.clinical_record_id = clinical_record_id
    control.professional_id = request.json.get("professional_id")

    db.session.add(control)
    db.session.commit()

    return jsonify({
        "msg": "control añadido correctamente"
    }), 200

@app.route("/get_all_controls", methods=["GET"])
def controls():
    control = Control.query.all()
    control_serialized = list(map( lambda control: control.serialize(), control))
    return jsonify(control_serialized)

@app.route("/get_controls", methods=["GET"])
@jwt_required()
def get_controls():
    patient_id = get_jwt_identity()
    control = Control.query.filter_by(clinical_record_id=patient_id).all()
    control_serialized = list(map( lambda control: control.serialize(), control))
    return jsonify(control_serialized)



@app.route("/add_habit", methods=["POST"])
def add_habit():
    habit = Habit()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    habit.name = request.json.get("name")
    habit.clinical_record_id = clinical_record_id

    db.session.add(habit)
    db.session.commit()

    return jsonify({
        "msg": "Habito añadido correctamente"
    }), 200

@app.route("/habit", methods=["GET"])
def habit():
    habit = Habit.query.all()
    habit_serialized = list(map( lambda habit: habit.serialize(), habit))
    return jsonify(habit_serialized)

@app.route("/habits", methods=["GET"])
@jwt_required()
def habits():
    patient_id = get_jwt_identity()
    habit = Habit.query.filter_by(clinical_record_id=patient_id).all()
    habit_serialized = list(map( lambda habit: habit.serialize(), habit))
    return jsonify(habit_serialized)

@app.route("/add_pathology", methods=["POST"])
def add_pathology():
    pathology = Pathology()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    pathology.name = request.json.get("name")
    pathology.clinical_record_id = clinical_record_id

    db.session.add(pathology)
    db.session.commit()

    return jsonify({
        "msg": "Patologia añadida correctamente"
    }), 200

@app.route("/pathology", methods=["GET"])
def pathology():
    pathology = Pathology.query.all()
    pathology_serialized = list(map( lambda pathology: pathology.serialize(), pathology))
    return jsonify(pathology_serialized)

@app.route("/pathologies", methods=["GET"])
@jwt_required()
def pathologies():
    patient_id = get_jwt_identity()
    pathology = Pathology.query.filter_by(clinical_record_id=patient_id).all()
    pathology_serialized = list(map( lambda pathology: pathology.serialize(), pathology))
    return jsonify(pathology_serialized)


@app.route("/add_surgery", methods=["POST"])
def add_surgery():
    surgery = Surgery()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    surgery.name = request.json.get("name")
    surgery.clinical_record_id = clinical_record_id

    db.session.add(surgery)
    db.session.commit()

    return jsonify({
        "msg": "Cirugia añadida correctamente"
    }), 200

@app.route("/surgery", methods=["GET"])
def surgery():
    surgery= Surgery.query.all()
    surgery_serialized = list(map( lambda surgery: surgery.serialize(), surgery))
    return jsonify(surgery_serialized)

@app.route("/surgeries", methods=["GET"])
@jwt_required()
def surgeries():
    patient_id = get_jwt_identity()
    surgery = Surgery.query.filter_by(clinical_record_id=patient_id).all()
    surgery_serialized = list(map( lambda surgery: surgery.serialize(), surgery))
    return jsonify(surgery_serialized)


@app.route("/add_alergy", methods=["POST"])
def add_alergy():
    alergy = Alergy()
    clinical_record_id = request.json.get("clinical_record_id")

    found_clinical_record = Clinical_record.query.filter_by(id=clinical_record_id).first()

    if found_clinical_record is None:
        return jsonify({
            "msg": "no existe esta ficha clínica"
        }), 400

    alergy.name = request.json.get("name")
    alergy.clinical_record_id = clinical_record_id

    db.session.add(alergy)
    db.session.commit()

    return jsonify({
        "msg": "Alergia añadida correctamente"
    }), 200

@app.route("/alergy", methods=["GET"])
def alergy():
    alergy =  Alergy.query.all()
    alergy_serialized = list(map( lambda alergy: alergy.serialize(),  alergy))
    return jsonify( alergy_serialized)

@app.route("/alergies", methods=["GET"])
@jwt_required()
def alergies():
    patient_id = get_jwt_identity()
    alergy = Alergy.query.filter_by(clinical_record_id=patient_id).all()
    alergy_serialized = list(map( lambda alergy: alergy.serialize(), alergy))
    return jsonify(alergy_serialized)


@app.route("/get_clinical_record/<int:id>", methods=["GET"])
@jwt_required()
def clinical_record_by_id(id):
    clinical_record = Clinical_record.query.get(id)
    clinical_record_serialized = clinical_record.serialize()
    return jsonify(clinical_record_serialized)


@app.route("/get_caregiver_by_id/<int:patient_id>", methods=["GET"])
@jwt_required()
def get_caregiver_by_id(patient_id):
    patient = Patient.query.get(patient_id)
    caregiver = Caregiver.query.filter_by(patient_id=patient_id).first()
    return jsonify(caregiver.serialize())


if __name__ == "__main__":
    app.run(host="localhost", port=8080)

